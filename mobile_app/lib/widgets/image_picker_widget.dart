import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

typedef OnImageSelected = Future<void> Function(File imageFile);

class ImagePickerWidget extends StatefulWidget {
  const ImagePickerWidget({
    super.key,
    required this.onImageSelected,
    required this.label,
    required this.icon,
    required this.source,
  });

  final OnImageSelected onImageSelected;
  final String label;
  final IconData icon;
  final ImageSource source;

  @override
  State<ImagePickerWidget> createState() => _ImagePickerWidgetState();
}

class _ImagePickerWidgetState extends State<ImagePickerWidget> {
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;

  String _permissionLabel() {
    return widget.source == ImageSource.camera ? 'camera' : 'gallery';
  }

  Future<bool> _requestPermission() async {
    if (widget.source == ImageSource.camera) {
      final status = await Permission.camera.request();
      return status.isGranted;
    }

    // Let image_picker open system gallery UI directly.
    return true;
  }

  Future<void> _pickImage() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final label = _permissionLabel();
      final granted = await _requestPermission();
      if (!granted) {
        if (!mounted) {
          return;
        }

        final isPermanentlyDenied = await Permission.camera.isPermanentlyDenied;
        if (!mounted) {
          return;
        }

        if (isPermanentlyDenied) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                '$label permission is permanently denied. Open app settings to allow it.',
              ),
              action: SnackBarAction(
                label: 'Settings',
                onPressed: () {
                  openAppSettings();
                },
              ),
            ),
          );
          return;
        }

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Permission denied. Please allow $label access.',
            ),
          ),
        );
        return;
      }

      final XFile? picked = await _picker.pickImage(
        source: widget.source,
        imageQuality: 90,
      );

      if (picked == null) {
        return;
      }

      await widget.onImageSelected(File(picked.path));
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Image selection failed: $error')),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: _isLoading ? null : _pickImage,
        icon: _isLoading
            ? const SizedBox(
                width: 18,
                height: 18,
                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
              )
            : Icon(widget.icon),
        label: Text(widget.label),
      ),
    );
  }
}
