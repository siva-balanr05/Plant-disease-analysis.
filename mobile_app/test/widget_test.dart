import 'package:flutter_test/flutter_test.dart';

import 'package:plant_disease_detector/main.dart';

void main() {
  testWidgets('App renders home title', (WidgetTester tester) async {
    await tester.pumpWidget(const PlantDiseaseApp());
    await tester.pump();

    expect(find.text('Plant Disease Detector'), findsOneWidget);
  });
}
