import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

String get baseUrl {
  if (kIsWeb) {
    return "http://localhost:8000";
  }

  if (Platform.isAndroid) {
    return "http://10.0.2.2:8000";
  }

  if (Platform.isIOS) {
    return "http://127.0.0.1:8000";
  }

  return "http://localhost:8000";
}

class ApiService {
  static Future<Map<String, dynamic>> predictDisease(File imageFile) async {
    try {
      final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/predict'));
      request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode != 200) {
        throw Exception('Prediction failed (${response.statusCode}): ${response.body}');
      }

      final decoded = jsonDecode(response.body);
      if (decoded is! Map<String, dynamic>) {
        throw Exception('Invalid response format from server');
      }

      return decoded;
    } catch (error) {
      throw Exception('Network or server error: $error');
    }
  }

  static Future<List<dynamic>> getHistory([int limit = 20]) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/history?limit=$limit'));
      if (response.statusCode != 200) {
        throw Exception('History request failed (${response.statusCode})');
      }

      final decoded = jsonDecode(response.body);
      if (decoded is! Map<String, dynamic>) {
        throw Exception('Invalid history response format');
      }

      final predictions = decoded['predictions'];
      if (predictions is! List<dynamic>) {
        throw Exception('Predictions data not found');
      }

      return predictions;
    } catch (error) {
      throw Exception('Unable to fetch history: $error');
    }
  }

  static Future<bool> checkHealth() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      if (response.statusCode != 200) {
        return false;
      }

      final decoded = jsonDecode(response.body);
      return decoded is Map<String, dynamic> && decoded['status'] == 'ok';
    } catch (_) {
      return false;
    }
  }
}
