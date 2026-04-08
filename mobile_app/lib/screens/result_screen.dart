import 'dart:io';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../widgets/result_card_widget.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({
    super.key,
    required this.imageFile,
    required this.result,
  });

  final File imageFile;
  final Map<String, dynamic> result;

  @override
  Widget build(BuildContext context) {
    final String disease = (result['disease'] ?? 'Unknown').toString();
    final double confidence = ((result['confidence'] ?? 0) as num).toDouble();
    final String timestamp = (result['timestamp'] ?? DateTime.now().toIso8601String()).toString();
    final String predictionId = (result['prediction_id'] ?? 'N/A').toString();

    final Map<String, dynamic> topK =
        (result['top_k'] is Map<String, dynamic>) ? result['top_k'] as Map<String, dynamic> : {};

    final bool isHealthy = disease.toLowerCase().contains('healthy');
    final DateTime parsedDate = DateTime.tryParse(timestamp)?.toLocal() ?? DateTime.now();

    return Scaffold(
      appBar: AppBar(title: const Text('Analysis Result')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: Image.file(imageFile, height: 220, fit: BoxFit.cover),
          ),
          const SizedBox(height: 14),
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    disease,
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: isHealthy ? Colors.green.shade700 : Colors.red.shade700,
                    ),
                  ),
                  const SizedBox(height: 12),
                  LinearProgressIndicator(
                    value: confidence.clamp(0.0, 1.0),
                    minHeight: 10,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  const SizedBox(height: 8),
                  Text('Confidence: ${(confidence * 100).toStringAsFixed(2)}%'),
                  const SizedBox(height: 8),
                  Text('Timestamp: ${DateFormat.yMMMd().add_jm().format(parsedDate)}'),
                  const SizedBox(height: 8),
                  Text('Prediction ID: $predictionId'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          ResultCardWidget(disease: disease, confidence: confidence, timestamp: timestamp),
          const SizedBox(height: 12),
          const Text(
            'Top-K Predictions',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          if (topK.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(12),
                child: Text('No top-k scores available.'),
              ),
            )
          else
            ...topK.entries.map(
              (entry) => ListTile(
                contentPadding: const EdgeInsets.symmetric(horizontal: 8),
                title: Text(entry.key),
                trailing: Text('${(((entry.value as num?) ?? 0) * 100).toStringAsFixed(2)}%'),
              ),
            ),
          const SizedBox(height: 18),
          Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Analyse Another'),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: OutlinedButton(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Offline mode active. Local history storage is not implemented yet.')),
                    );
                  },
                  child: const Text('View History'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
