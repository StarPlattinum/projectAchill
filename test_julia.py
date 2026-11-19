import random, time
from julia import load_model

engine = load_model(r"C:\Users\PC\Julia-1", device="cpu", strict_encoding=True,
                    max_length=512, head_length=256)

def truth(x, size, obs):
    pos = "left" if x < 0.35 else "right" if x > 0.65 else "center"
    dist = "close" if size > 0.35 else "far" if size < 0.15 else "medium"
    return pos, dist, "yes" if obs else "no"

def describe(x, size, obs):
    pos = "on the left side" if x < 0.35 else "on the right side" if x > 0.65 else "in the center"
    dist = "very close to the robot" if size > 0.35 else "far away from the robot" if size < 0.15 else "at medium distance from the robot"
    o = "There is an obstacle right in front of the robot." if obs else "The path ahead is free."
    return f"The target bottle is {pos} of the camera image and {dist}. {o}"

questions = {
    "position": {"type": "choice", "instructions": "Where is the target in the image?",
        "criteria": {"left": "the target is on the left side",
                     "center": "the target is in the center",
                     "right": "the target is on the right side"}},
    "distance": {"type": "choice", "instructions": "How far is the target from the robot?",
        "criteria": {"far": "the target is far away from the robot",
                     "medium": "the target is at medium distance from the robot",
                     "close": "the target is very close to the robot"}},
    "obstacle": {"type": "choice", "instructions": "Is there an obstacle in front of the robot?",
        "criteria": {"no": "the path ahead is free",
                     "yes": "there is an obstacle in front of the robot"}},
}

random.seed(0)
N = 200
correct = {"position": 0, "distance": 0, "obstacle": 0}
times = []
for _ in range(N):
    x, size, obs = random.random(), random.uniform(0.03, 0.6), random.random() < 0.3
    t = time.time()
    a = engine.predict(state=describe(x, size, obs), questions=questions)["answers"]
    times.append((time.time() - t) * 1000)
    for k, g in zip(["position", "distance", "obstacle"], truth(x, size, obs)):
        correct[k] += a[k]["choice"] == g

for k, v in correct.items():
    print(f"{k}: {v}/{N} = {v / N:.1%}")
print(f"mean latency: {sum(times) / len(times):.0f} ms")