class DiseaseSolution {
  const DiseaseSolution({required this.title, required this.steps});
  final String title;
  final List<String> steps;
}

const _solutionRules = <_SolutionRule>[
  _SolutionRule(matchers: ['healthy'], solution: DiseaseSolution(
    title: 'Plant looks healthy',
    steps: [
      'Keep watering consistent and avoid waterlogging.',
      'Apply balanced fertilizer as per crop stage.',
      'Inspect leaves weekly to catch early disease signs.',
    ],
  )),
  _SolutionRule(matchers: ['late blight'], solution: DiseaseSolution(
    title: 'Control late blight',
    steps: [
      'Remove and destroy infected leaves immediately.',
      'Avoid overhead watering and improve air circulation.',
      'Apply a registered fungicide for late blight at recommended intervals.',
      'Rotate crops and avoid planting susceptible crops in the same area next season.',
    ],
  )),
  _SolutionRule(matchers: ['early blight'], solution: DiseaseSolution(
    title: 'Control early blight',
    steps: [
      'Prune lower infected leaves and sanitize tools after use.',
      'Mulch around plants to reduce soil splash.',
      'Use preventive fungicide sprays if weather is warm and humid.',
      'Maintain balanced nutrition, especially potassium.',
    ],
  )),
  _SolutionRule(matchers: ['septoria leaf spot'], solution: DiseaseSolution(
    title: 'Manage septoria leaf spot',
    steps: [
      'Remove heavily infected foliage and debris from the field.',
      'Water at the base of plants in the morning.',
      'Use protective fungicide where disease pressure is high.',
      'Rotate away from tomato and related crops for 2-3 seasons.',
    ],
  )),
  _SolutionRule(matchers: ['bacterial spot'], solution: DiseaseSolution(
    title: 'Manage bacterial spot',
    steps: [
      'Remove infected leaves and avoid handling wet plants.',
      'Use clean seed/seedlings and disinfect tools regularly.',
      'Apply copper-based bactericide where recommended.',
      'Improve spacing to reduce leaf wetness duration.',
    ],
  )),
  _SolutionRule(matchers: ['leaf mold'], solution: DiseaseSolution(
    title: 'Manage leaf mold',
    steps: [
      'Increase ventilation and reduce humidity around plants.',
      'Remove affected leaves to limit spread.',
      'Water early in the day and keep foliage dry.',
      'Use resistant varieties and fungicide if needed.',
    ],
  )),
  _SolutionRule(matchers: ['powdery mildew'], solution: DiseaseSolution(
    title: 'Control powdery mildew',
    steps: [
      'Prune dense canopy to improve airflow.',
      'Remove leaves with heavy white growth.',
      'Apply sulfur or other labeled fungicide at first signs.',
      'Avoid excess nitrogen that encourages dense, susceptible growth.',
    ],
  )),
  _SolutionRule(matchers: ['mosaic virus'], solution: DiseaseSolution(
    title: 'Manage mosaic virus',
    steps: [
      'Remove infected plants promptly; viral diseases are not curable.',
      'Control aphids and other vectors that spread the virus.',
      'Disinfect hands/tools and avoid tobacco contamination.',
      'Use resistant varieties in future planting.',
    ],
  )),
  _SolutionRule(matchers: ['target spot'], solution: DiseaseSolution(
    title: 'Manage target spot',
    steps: [
      'Scout frequently and remove early infected leaves.',
      'Reduce leaf wetness with drip irrigation and spacing.',
      'Use crop-approved fungicides with rotation of active ingredients.',
      'Clear crop residue after harvest.',
    ],
  )),
  _SolutionRule(matchers: ['rust'], solution: DiseaseSolution(
    title: 'Manage rust disease',
    steps: [
      'Remove heavily infected leaves where practical.',
      'Avoid prolonged moisture on foliage.',
      'Apply crop-labeled fungicide if rust is spreading quickly.',
      'Plant resistant varieties for the next cycle.',
    ],
  )),
  _SolutionRule(matchers: ['scab'], solution: DiseaseSolution(
    title: 'Manage scab disease',
    steps: [
      'Remove and destroy fallen infected leaves.',
      'Apply fungicide during early growth stages.',
      'Prune trees to increase air circulation.',
      'Use resistant varieties where available.',
    ],
  )),
  _SolutionRule(matchers: ['black rot'], solution: DiseaseSolution(
    title: 'Control black rot',
    steps: [
      'Remove and destroy infected plant parts immediately.',
      'Avoid overhead irrigation and improve air circulation.',
      'Apply appropriate fungicide during the growing season.',
      'Practice crop rotation and use disease-free seeds.',
    ],
  )),
  _SolutionRule(matchers: ['leaf scorch'], solution: DiseaseSolution(
    title: 'Manage leaf scorch',
    steps: [
      'Ensure adequate and consistent watering.',
      'Mulch around plants to retain soil moisture.',
      'Remove severely scorched leaves to reduce stress.',
      'Avoid excessive fertilizer application.',
    ],
  )),
  _SolutionRule(matchers: ['citrus greening'], solution: DiseaseSolution(
    title: 'Manage citrus greening (HLB)',
    steps: [
      'Remove and destroy infected trees to prevent spread.',
      'Control Asian citrus psyllid vectors with approved insecticides.',
      'Use certified disease-free nursery stock.',
      'Monitor trees regularly for early symptoms.',
    ],
  )),
  _SolutionRule(matchers: ['spider mite', 'two-spotted'], solution: DiseaseSolution(
    title: 'Control spider mites',
    steps: [
      'Spray plants with strong water jets to dislodge mites.',
      'Introduce natural predators like ladybugs or predatory mites.',
      'Apply miticide or insecticidal soap if infestation is severe.',
      'Keep plants well-watered; mites thrive in dry conditions.',
    ],
  )),
  _SolutionRule(matchers: ['yellow leaf curl'], solution: DiseaseSolution(
    title: 'Manage yellow leaf curl virus',
    steps: [
      'Remove and destroy infected plants immediately.',
      'Control whitefly populations with sticky traps and insecticides.',
      'Use virus-resistant tomato varieties.',
      'Use reflective mulch to repel whiteflies.',
    ],
  )),
  _SolutionRule(matchers: ['esca', 'black measles'], solution: DiseaseSolution(
    title: 'Manage esca / black measles',
    steps: [
      'Prune infected vines during dry weather and seal wounds.',
      'Remove severely affected vines from the vineyard.',
      'Avoid pruning during wet conditions to limit fungal entry.',
      'Use preventive trunk treatments where available.',
    ],
  )),
  _SolutionRule(matchers: ['isariopsis', 'leaf spot'], solution: DiseaseSolution(
    title: 'Manage leaf spot disease',
    steps: [
      'Remove and destroy infected leaves promptly.',
      'Avoid overhead watering to keep foliage dry.',
      'Apply fungicide at the first sign of spots.',
      'Ensure good spacing for air circulation.',
    ],
  )),
  _SolutionRule(matchers: ['cercospora', 'gray leaf spot'], solution: DiseaseSolution(
    title: 'Manage cercospora / gray leaf spot',
    steps: [
      'Use resistant hybrids where available.',
      'Rotate crops away from corn for at least one season.',
      'Apply foliar fungicide if disease is progressing.',
      'Reduce crop residue through tillage after harvest.',
    ],
  )),
  _SolutionRule(matchers: ['common rust'], solution: DiseaseSolution(
    title: 'Control common rust in corn',
    steps: [
      'Plant resistant corn hybrids.',
      'Apply fungicide if rust appears before tasseling.',
      'Scout fields regularly during warm, humid weather.',
      'Remove volunteer corn that may harbor the fungus.',
    ],
  )),
  _SolutionRule(matchers: ['northern leaf blight'], solution: DiseaseSolution(
    title: 'Manage northern leaf blight',
    steps: [
      'Use resistant corn hybrids.',
      'Apply foliar fungicide at early disease onset.',
      'Rotate crops and reduce corn residue.',
      'Monitor fields during moderate temperatures and wet conditions.',
    ],
  )),
];

const _fallbackSolution = DiseaseSolution(
  title: 'General disease management',
  steps: [
    'Isolate affected plants and remove severely infected tissue.',
    'Keep leaves dry and improve ventilation around plants.',
    'Use crop-specific fungicide/bactericide only after label verification.',
    'Consult local agronomy guidance for region-specific treatment plans.',
  ],
);

DiseaseSolution getDiseaseSolution(String diseaseName) {
  final normalized = diseaseName.toLowerCase();
  for (final rule in _solutionRules) {
    if (rule.matchers.any((m) => normalized.contains(m))) {
      return rule.solution;
    }
  }
  return _fallbackSolution;
}

class _SolutionRule {
  const _SolutionRule({required this.matchers, required this.solution});
  final List<String> matchers;
  final DiseaseSolution solution;
}
