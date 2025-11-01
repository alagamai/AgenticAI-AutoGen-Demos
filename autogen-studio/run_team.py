import json
from autogen_agentchat.teams import RoundRobinGroupChat

# Load your saved team config
with open(".autogenstudio/teams/math_classroom_team.json") as f:
    team_data = json.load(f)

# Create the team from saved config
team = RoundRobinGroupChat.from_dict(team_data["config"])

# Start the conversation
print("🎓 Starting the Math Classroom Team...")
team.run()

