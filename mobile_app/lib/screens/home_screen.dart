import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/api_service.dart';
import '../widgets/image_picker_widget.dart';
import 'result_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isConnected = false;
  bool _checkingConnection = true;
  bool _predicting = false;

  @override
  void initState() {
    super.initState();
    _checkHealth();
  }

  Future<void> _checkHealth() async {
    setState(() {
      _checkingConnection = true;
    });

    final connected = await ApiService.checkHealth();
    if (!mounted) {
      return;
    }

    setState(() {
      _isConnected = connected;
      _checkingConnection = false;
    });
  }

  Future<void> _onImageSelected(File imageFile) async {
    setState(() {
      _predicting = true;
    });

    try {
      final result = await ApiService.predictDisease(imageFile);
      if (!mounted) {
        return;
      }
      await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(imageFile: imageFile, result: result),
        ),
      );
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Prediction failed: $error')),
      );
    } finally {
      if (mounted) {
        setState(() {
          _predicting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Plant Disease Detector')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Icon(Icons.eco, color: Colors.green.shade600, size: 90),
                const SizedBox(height: 12),
                const Text(
                  'Offline Plant Disease Detection',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      if (_checkingConnection)
                        const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      else
                        Icon(
                          Icons.circle,
                          size: 12,
                          color: _isConnected ? Colors.green : Colors.red,
                        ),
                      const SizedBox(width: 8),
                      Text(
                        _checkingConnection
                            ? 'Checking API connection...'
                            : (_isConnected ? 'API Connected' : 'API Not Reachable'),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                if (_predicting)
                  const Padding(
                    padding: EdgeInsets.only(bottom: 12),
                    child: Center(child: CircularProgressIndicator()),
                  ),
                ImagePickerWidget(
                  onImageSelected: _onImageSelected,
                  label: 'Open Camera',
                  icon: Icons.camera_alt,
                  source: ImageSource.camera,
                ),
                const SizedBox(height: 12),
                ImagePickerWidget(
                  onImageSelected: _onImageSelected,
                  label: 'Choose from Gallery',
                  icon: Icons.photo_library,
                  source: ImageSource.gallery,
                ),
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: _checkingConnection ? null : _checkHealth,
                  icon: const Icon(Icons.sync),
                  label: const Text('Refresh Connection Status'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
