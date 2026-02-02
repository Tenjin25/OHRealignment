import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the statewide races section
content = re.sub(
    r'<p><strong>Statewide Races Tell the Same Story - The Superminority Emerges:</strong></p>\s*<ul>.*?</ul>',
    '''<p><strong>Key Statewide Races:</strong></p>
            <ul>
              <li><strong>2006 U.S. Senate:</strong> Sherrod Brown (D) 56.2%, Mike DeWine (R) 43.8%</li>
              <li><strong>2010 Governor:</strong> John Kasich (R) 49.0%, Ted Strickland (D) 46.9%</li>
              <li><strong>2010 U.S. Senate:</strong> Rob Portman (R) 57.0%, Lee Fisher (D) 39.0%</li>
              <li><strong>2018 U.S. Senate:</strong> Sherrod Brown (D) 53.4%, Jim Renacci (R) 46.6%</li>
              <li><strong>2022 U.S. Senate:</strong> J.D. Vance (R) 53.3%, Tim Ryan (D) 46.7% — Vance elected VP in 2024</li>
              <li><strong>2022 Governor:</strong> Mike DeWine (R) 62.8%, Nan Whaley (D) 37.2%</li>
            </ul>''',
    content,
    flags=re.DOTALL
)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleanup complete!")
