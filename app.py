import gradio as gr

# Means and standard deviations from Loft data
MEANS = {
    'engagement_depth': 4162.714529,
    'exploration_breadth': 3.161074,
    'decision_momentum': -1.951359,
    'revisit_intensity': 4.019175
}
STDS = {
    'engagement_depth': 45539.847327,
    'exploration_breadth': 2.044317,
    'decision_momentum': 4.805851,
    'revisit_intensity': 8.309891
}

# ICP weight definitions
WEIGHTS = {
    'Deep Divers':            {'norm_depth':  1,  'norm_breadth':  1,  'norm_momentum':  0,  'norm_revisit':  0},
    'Rapid Deciders':         {'norm_depth': -1,  'norm_breadth': -1,  'norm_momentum':  1,  'norm_revisit':  0},
    'Looping Doubters':       {'norm_depth':  0,  'norm_breadth':  0,  'norm_momentum': -1,  'norm_revisit':  1},
    'Comprehensive Auditors': {'norm_depth':  1,  'norm_breadth':  1,  'norm_momentum':  1,  'norm_revisit':  1},
    'Surface Samplers':       {'norm_depth': -1,  'norm_breadth': -1,  'norm_momentum':  0,  'norm_revisit':  0},
}

def normalize(val, mean, std):
    return (val - mean) / std if std else 0

def assign_icp(engagement, breadth, momentum, revisit):
    # Normalize inputs
    norm = {
        'norm_depth':     normalize(engagement, MEANS['engagement_depth'],     STDS['engagement_depth']),
        'norm_breadth':   normalize(breadth,   MEANS['exploration_breadth'],  STDS['exploration_breadth']),
        'norm_momentum':  normalize(momentum,  MEANS['decision_momentum'],    STDS['decision_momentum']),
        'norm_revisit':   normalize(revisit,   MEANS['revisit_intensity'],    STDS['revisit_intensity']),
    }
    # Score each ICP
    scores = {icp: sum(norm[k]*w for k,w in WEIGHTS[icp].items()) for icp in WEIGHTS}
    # Pick max
    chosen = max(scores, key=scores.get)
    return chosen, scores

iface = gr.Interface(
    fn=assign_icp,
    inputs=[
      gr.inputs.Number(label="Engagement Depth (sec)", default=0.0),
      gr.inputs.Number(label="Exploration Breadth (pages)", default=0),
      gr.inputs.Number(label="Decision Momentum", default=0.0),
      gr.inputs.Number(label="Revisit Intensity", default=0)
    ],
    outputs=[
      gr.outputs.Textbox(label="Assigned ICP"),
      gr.outputs.JSON(label="All ICP Scores")
    ],
    title="Loft ICP Assignment",
    description="Enter a lead's metrics to see its ICP segment."
)

if __name__ == "__main__":
    iface.launch()
