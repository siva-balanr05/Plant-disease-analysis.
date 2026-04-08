const SOLUTION_RULES = [
  {
    matchers: ["healthy"],
    title: "Plant looks healthy",
    steps: [
      "Keep watering consistent and avoid waterlogging.",
      "Apply balanced fertilizer as per crop stage.",
      "Inspect leaves weekly to catch early disease signs.",
    ],
  },
  {
    matchers: ["late blight"],
    title: "Control late blight",
    steps: [
      "Remove and destroy infected leaves immediately.",
      "Avoid overhead watering and improve air circulation.",
      "Apply a registered fungicide for late blight at recommended intervals.",
      "Rotate crops and avoid planting susceptible crops in the same area next season.",
    ],
  },
  {
    matchers: ["early blight"],
    title: "Control early blight",
    steps: [
      "Prune lower infected leaves and sanitize tools after use.",
      "Mulch around plants to reduce soil splash.",
      "Use preventive fungicide sprays if weather is warm and humid.",
      "Maintain balanced nutrition, especially potassium.",
    ],
  },
  {
    matchers: ["septoria leaf spot"],
    title: "Manage septoria leaf spot",
    steps: [
      "Remove heavily infected foliage and debris from the field.",
      "Water at the base of plants in the morning.",
      "Use protective fungicide where disease pressure is high.",
      "Rotate away from tomato and related crops for 2-3 seasons.",
    ],
  },
  {
    matchers: ["bacterial spot"],
    title: "Manage bacterial spot",
    steps: [
      "Remove infected leaves and avoid handling wet plants.",
      "Use clean seed/seedlings and disinfect tools regularly.",
      "Apply copper-based bactericide where recommended.",
      "Improve spacing to reduce leaf wetness duration.",
    ],
  },
  {
    matchers: ["leaf mold"],
    title: "Manage leaf mold",
    steps: [
      "Increase ventilation and reduce humidity around plants.",
      "Remove affected leaves to limit spread.",
      "Water early in the day and keep foliage dry.",
      "Use resistant varieties and fungicide if needed.",
    ],
  },
  {
    matchers: ["powdery mildew"],
    title: "Control powdery mildew",
    steps: [
      "Prune dense canopy to improve airflow.",
      "Remove leaves with heavy white growth.",
      "Apply sulfur or other labeled fungicide at first signs.",
      "Avoid excess nitrogen that encourages dense, susceptible growth.",
    ],
  },
  {
    matchers: ["mosaic virus"],
    title: "Manage mosaic virus",
    steps: [
      "Remove infected plants promptly; viral diseases are not curable.",
      "Control aphids and other vectors that spread the virus.",
      "Disinfect hands/tools and avoid tobacco contamination.",
      "Use resistant varieties in future planting.",
    ],
  },
  {
    matchers: ["target spot"],
    title: "Manage target spot",
    steps: [
      "Scout frequently and remove early infected leaves.",
      "Reduce leaf wetness with drip irrigation and spacing.",
      "Use crop-approved fungicides with rotation of active ingredients.",
      "Clear crop residue after harvest.",
    ],
  },
  {
    matchers: ["rust"],
    title: "Manage rust disease",
    steps: [
      "Remove heavily infected leaves where practical.",
      "Avoid prolonged moisture on foliage.",
      "Apply crop-labeled fungicide if rust is spreading quickly.",
      "Plant resistant varieties for the next cycle.",
    ],
  },
];

const FALLBACK_SOLUTION = {
  title: "General disease management",
  steps: [
    "Isolate affected plants and remove severely infected tissue.",
    "Keep leaves dry and improve ventilation around plants.",
    "Use crop-specific fungicide/bactericide only after label verification.",
    "Consult local agronomy guidance for region-specific treatment plans.",
  ],
};

export function getDiseaseSolution(diseaseName) {
  const normalized = (diseaseName || "").toLowerCase();

  for (const rule of SOLUTION_RULES) {
    const matched = rule.matchers.some((matcher) => normalized.includes(matcher));
    if (matched) {
      return rule;
    }
  }

  return FALLBACK_SOLUTION;
}
