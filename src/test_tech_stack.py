from collectors.tech_stack import detect_tech_stack

url = "https://www.americanhorizonproperty.com/"
stack = detect_tech_stack(url)

for key, value in stack.items():
    print(f"{key}: {value}")
