import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class ResultCardWidget extends StatelessWidget {
  const ResultCardWidget({
    super.key,
    required this.disease,
    required this.confidence,
    required this.timestamp,
  });

  final String disease;
  final double confidence;
  final String timestamp;

  @override
  Widget build(BuildContext context) {
    final bool isHealthy = disease.toLowerCase().contains('healthy');
    final DateTime parsedDate = DateTime.tryParse(timestamp)?.toLocal() ?? DateTime.now();

    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              disease,
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: isHealthy ? Colors.green.shade700 : Colors.red.shade700,
              ),
            ),
            const SizedBox(height: 10),
            TweenAnimationBuilder<double>(
              tween: Tween<double>(begin: 0, end: confidence.clamp(0.0, 1.0)),
              duration: const Duration(milliseconds: 800),
              builder: (context, value, child) {
                return LinearProgressIndicator(
                  value: value,
                  minHeight: 10,
                  borderRadius: BorderRadius.circular(8),
                );
              },
            ),
            const SizedBox(height: 8),
            Text('${(confidence * 100).toStringAsFixed(2)}% confidence'),
            const SizedBox(height: 8),
            Text('Detected: ${DateFormat.yMMMd().add_jm().format(parsedDate)}'),
          ],
        ),
      ),
    );
  }
}
