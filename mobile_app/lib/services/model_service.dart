import 'dart:io';
import 'dart:math';

import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';

class ModelService {
  ModelService._();

  static final ModelService instance = ModelService._();

  static const String _modelAssetPath = 'assets/models/plant_disease.tflite';
  static const String _labelsAssetPath = 'assets/models/labels.txt';
  static const int _defaultInputSize = 224;
  static const int _topK = 5;

  Interpreter? _interpreter;
  List<String> _labels = const [];

  Future<void> initialize() async {
    if (_interpreter != null && _labels.isNotEmpty) {
      return;
    }

    // Load model bytes from Flutter asset bundle and create interpreter
    final modelData = await rootBundle.load(_modelAssetPath);
    final buffer = modelData.buffer.asUint8List();
    _interpreter = Interpreter.fromBuffer(buffer);
    _labels = await _loadLabels(_labelsAssetPath);

    final outputShape = _interpreter!.getOutputTensor(0).shape;
    final outputClasses = outputShape.isNotEmpty ? outputShape.last : _labels.length;

    if (_labels.isEmpty) {
      throw Exception('No labels found in $_labelsAssetPath');
    }

    if (outputClasses != _labels.length) {
      throw Exception(
        'Label count (${_labels.length}) does not match model output classes ($outputClasses).',
      );
    }
  }

  Future<Map<String, dynamic>> predictDisease(File imageFile) async {
    await initialize();

    final bytes = await imageFile.readAsBytes();
    final decoded = img.decodeImage(bytes);
    if (decoded == null) {
      throw Exception('Unable to decode selected image.');
    }

    final resized = img.copyResize(decoded, width: _defaultInputSize, height: _defaultInputSize);

    final input = _buildInputTensor(resized);
    final output = List.generate(1, (_) => List.filled(_labels.length, 0.0));

    _interpreter!.run(input, output);

    final logits = List<double>.from(output[0].map((e) => (e as num).toDouble()));
    final probs = _softmax(logits);
    final ranked = _rankPredictions(probs);

    final top = ranked.first;
    final topKEntries = ranked.take(_topK);

    final topKMap = <String, double>{
      for (final entry in topKEntries) _labels[entry.index]: entry.score,
    };

    return {
      'disease': _labels[top.index],
      'confidence': top.score,
      'timestamp': DateTime.now().toUtc().toIso8601String(),
      'prediction_id': _localPredictionId(),
      'top_k': topKMap,
    };
  }

  Future<bool> checkModelReady() async {
    try {
      await initialize();
      return true;
    } catch (_) {
      return false;
    }
  }

  void dispose() {
    _interpreter?.close();
    _interpreter = null;
  }

  List<List<List<List<double>>>> _buildInputTensor(img.Image image) {
    final input = List.generate(
      1,
      (_) => List.generate(
        _defaultInputSize,
        (y) => List.generate(_defaultInputSize, (x) {
          final pixel = image.getPixel(x, y);
          final r = ((pixel.r / 255.0) - 0.5) / 0.5;
          final g = ((pixel.g / 255.0) - 0.5) / 0.5;
          final b = ((pixel.b / 255.0) - 0.5) / 0.5;
          return [r, g, b];
        }),
      ),
    );

    return input;
  }

  List<double> _softmax(List<double> logits) {
    final maxLogit = logits.reduce(max);
    final exps = logits.map((x) => exp(x - maxLogit)).toList(growable: false);
    final sumExps = exps.reduce((a, b) => a + b);

    return exps.map((x) => x / sumExps).toList(growable: false);
  }

  List<_ScoredIndex> _rankPredictions(List<double> probs) {
    final scored = <_ScoredIndex>[];
    for (var i = 0; i < probs.length; i++) {
      scored.add(_ScoredIndex(index: i, score: probs[i]));
    }
    scored.sort((a, b) => b.score.compareTo(a.score));
    return scored;
  }

  Future<List<String>> _loadLabels(String assetPath) async {
    final raw = await rootBundle.loadString(assetPath);
    return raw
        .split('\n')
        .map((line) => line.trim())
        .where((line) => line.isNotEmpty)
        .toList(growable: false);
  }

  String _localPredictionId() {
    final now = DateTime.now().millisecondsSinceEpoch;
    final randomSuffix = Random().nextInt(100000).toString().padLeft(5, '0');
    return 'local-$now-$randomSuffix';
  }
}

class _ScoredIndex {
  _ScoredIndex({required this.index, required this.score});

  final int index;
  final double score;
}
