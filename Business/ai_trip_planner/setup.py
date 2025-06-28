from typing_extensions import List

def get_requirements()->List[str]:
    """
    returns requirements as a list
    """
    requirements_list: List[str] = []

    try:
        with open("requirements.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                requirements_list.append(requirement)
            return requirements_list
    except Exception as e:
        return f"Error: {str(e)}"