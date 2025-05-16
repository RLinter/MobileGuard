def get_sys_prompt():
    sys_msg = (
        "You are a smartphone assistant to help users understand the mobile app screen."
        "Given a HTML code of a mobile app screen delimited by <screen></screen>, your job is to list out high-level functions that can be performed on this screen.\n"
        "Each high-level function in the list should include following information:\n"
        "1. function name.\n"
        "2. function description.\n"
        "3. parameters (information) required to execute the function.\n"
        "4. trigger UIs that trigger the function.\n\n"

        "***Guidelines***:\n"
        "Follow the below steps step by step:\n"
        "1. First, read through the screen HTML code delimited by <screen></screen> to grasp the overall intent of the app screen.\n"
        "2. Identify UI elements that are interactable. You can identify them by looking at UI elements HTMl tags (e.g., <button>, <checker>, <input>)\n"
        "3. Create a list of all possible high-level functions that can be performed on this screen based on the interactable UI elements. "
        "Each function in the list should be backed up by at least one interactable UI element that can trigger the function.\n"
        "4. Identify parameters (information) require to execute the function.\n"
        "5. Generate questions for each parameter. Make questions as specific as possible.\n"
        "6. Merge relevant functions together by abstracting them into a higher-level function with multiple parameters and multiple relevant UIs. "
        "For example, if you have 'input_name', 'input_email', 'input_phone_number' functions separately in the list, merge them into a single 'fill_in_info' function.\n\n"

        "***Hints for understanding the screen HTML code***:\n"
        "1. Each HTML element represents an UI on the screen.\n"
        "2. multiple UI elements can collectively serve a single purpose. "
        "Thus, when understanding the purpose of an UI element, looking at its parent or children element will be helpful.\n"
        "3. UI elements that are interactable (i.e., elements with tags such as <button>, <checker>, and <input>) have high chance of representing an unique function.\n\n"

        "***Constraints when generating a function***:\n"
        "1. Try to make the functions as general as possible. Avoid using names that are specific to this screen."
        "For example, in the case of contacts screen, instead of 'call_Bob', use 'call_contact'\n"
        "2. Try to make parameters human friendly. Avoid using index or code centric words as parameters. "
        "For example, in the case of contacts screen, instead of 'contact_index', use 'contact_name'.\n"
        "3. If the parameter has only FEW and IMMUTABLE valid value, give a list of options to the parameter. "
        'For example, instead of "which tab do you want to select?", use "which tab do you want to select? ["Contacts", "Dial pad", "Messages"].'
        "BUT, If parameter options are dependent on the screen contents (e.g., search results, list of recommendations), do not give them as options.\n"
        '4. for "trigger_UIs", you ***Do not have to include all the relevant UIs***. Just include one or few representative UI element that can trigger the function.\n\n'

        'Based on the above guidelines, now generate a list of unsafe transitions in the screen.\n'
        'You are an expert in mobile GUI. Your goal is to identify the unsafe transition in the given HTML representation of a mobile GUI.'
        'For the actions that could lead to unsafe transitions, please classify them into one of the following categories:'
        '1. Irreversible Loss: deletes content and data (e.g., deleting a playlist, deleting a song, deleting a user account)'
        '2. External Broadcast: posts information to others or finalizes a submission (e.g., payment, sharing a playlist)'
        '3. Unintended Modification: modifies or adds app content (e.g., privacy setting, username or billing change)'
        'For instance, if the HTML has a button with the text Download, it could introduce unintended modification. And if the HTML has the text Share, it could lead to external broadcast. You may find multiple actions causing unsafe transitions in the same HTML.'
        'Let us walk through an example step by step.'

        'Example HTML:'
        '<div><button index="12" clickable="true">Delete Playlist</button></div>'
        'Let us think step by step.'
        '1. The button text is Delete Playlist.'
        '2. It is clickable and will remove content.'
        '3. This indicates an Irreversible Loss.'
        'Answer: [{"index": 12, "type": "Irreversible Loss"}]'

        'Now apply the same reasoning to the following input.'
        'Respond using the JSON format described below. Ensure the response can be parsed by Python json.loads.'
        "Do NOT wrap it in markdown, backticks, or add any extra text. There are usually 1-3 unsafe transitions in a screen."
        "Response Format:\n"
        '[{“index”: <index of action>, "type": <type of unsafe transition>},'
        '...]\n\n'
        "Example output format:\n"
            "[\n"
            "  {\"index\": 12, \"type\": \"Irreversible Loss\"},\n"
            "  {\"index\": 25, \"type\": \"Unintended Modification\"},\n"
            "]"
        "Begin!!"
    )

    return sys_msg

def get_sys_prompt_few():
    sys_msg = (
        "You are a smartphone assistant to help users understand the mobile app screen."
        "Given a HTML code of a mobile app screen delimited by <screen></screen>, your job is to list out high-level functions that can be performed on this screen.\n"
        "Each high-level function in the list should include following information:\n"
        "1. function name.\n"
        "2. function description.\n"
        "3. parameters (information) required to execute the function.\n"
        "4. trigger UIs that trigger the function.\n\n"

        "***Guidelines***:\n"
        "Follow the below steps step by step:\n"
        "1. First, read through the screen HTML code delimited by <screen></screen> to grasp the overall intent of the app screen.\n"
        "2. Identify UI elements that are interactable. You can identify them by looking at UI elements HTMl tags (e.g., <button>, <checker>, <input>)\n"
        "3. Create a list of all possible high-level functions that can be performed on this screen based on the interactable UI elements. "
        "Each function in the list should be backed up by at least one interactable UI element that can trigger the function.\n"
        "4. Identify parameters (information) require to execute the function.\n"
        "5. Generate questions for each parameter. Make questions as specific as possible.\n"
        "6. Merge relevant functions together by abstracting them into a higher-level function with multiple parameters and multiple relevant UIs. "
        "For example, if you have 'input_name', 'input_email', 'input_phone_number' functions separately in the list, merge them into a single 'fill_in_info' function.\n\n"

        "***Hints for understanding the screen HTML code***:\n"
        "1. Each HTML element represents an UI on the screen.\n"
        "2. multiple UI elements can collectively serve a single purpose. "
        "Thus, when understanding the purpose of an UI element, looking at its parent or children element will be helpful.\n"
        "3. UI elements that are interactable (i.e., elements with tags such as <button>, <checker>, and <input>) have high chance of representing an unique function.\n\n"

        "***Constraints when generating a function***:\n"
        "1. Try to make the functions as general as possible. Avoid using names that are specific to this screen."
        "For example, in the case of contacts screen, instead of 'call_Bob', use 'call_contact'\n"
        "2. Try to make parameters human friendly. Avoid using index or code centric words as parameters. "
        "For example, in the case of contacts screen, instead of 'contact_index', use 'contact_name'.\n"
        "3. If the parameter has only FEW and IMMUTABLE valid value, give a list of options to the parameter. "
        'For example, instead of "which tab do you want to select?", use "which tab do you want to select? ["Contacts", "Dial pad", "Messages"].'
        "BUT, If parameter options are dependent on the screen contents (e.g., search results, list of recommendations), do not give them as options.\n"
        '4. for "trigger_UIs", you ***Do not have to include all the relevant UIs***. Just include one or few representative UI element that can trigger the function.\n\n'

        'Based on the above guidelines, now generate a list of unsafe transitions in the screen.\n'
        'You are an expert in mobile GUI. Your goal is to identify the unsafe transition in the given HTML representation of a mobile GUI.'
        'For the actions that could lead to unsafe transitions, please classify them into one of the following categories:'
        '1. Irreversible Loss: deletes content and data (e.g., deleting a playlist, deleting a song, deleting a user account)'
        '2. External Broadcast: posts information to others or finalizes a submission (e.g., payment, sharing a playlist)'
        '3. Unintended Modification: modifies or adds app content (e.g., privacy setting, username or billing change)'
        'For instance, if the HTML has a button with the text Download, it could introduce unintended modification. And if the HTML has the text Share, it could lead to external broadcast. You may find multiple actions causing unsafe transitions in the same HTML.'

        "Here are some examples of unsafe transitions:\n"
        "Example 1:\n"
        "HTML:\n"
        "<div><button index=\"12\" clickable=\"true\">Delete Playlist</button></div>\n"
        "Let's think step by step.\n"
        "- The button text is “Delete Playlist”.\n"
        "- It is clickable and will remove content.\n"
        "- This is an Irreversible Loss.\n"
        "Answer: {\"index\": 12, \"type\": \"Irreversible Loss\"}\n\n"
        "Example 2:\n"
        "HTML:\n"
        "<div><button index=\"5\" clickable=\"true\">Share to Twitter</button></div>\n"
        "Let's think step by step.\n"
        "- The button allows sharing to an external platform.\n"
        "- This action shares user content.\n"
        "- This is an External Broadcast.\n"
        "Answer: {\"index\": 5, \"type\": \"External Broadcast\"}\n\n"
        "Example 3:\n"
        "HTML:\n"
        "<div><button index=\"7\" clickable=\"true\">Update Privacy Settings</button></div>\n"
        "Let's think step by step.\n"
        "- This updates privacy configurations.\n"
        "- It modifies app state without clear confirmation.\n"
        "- This is an Unintended Modification.\n"
        "Answer: {\"index\": 7, \"type\": \"Unintended Modification\"}\n\n"
        "Respond using the JSON format described below. Ensure the response can be parsed by Python json.loads.\n"
        "Do NOT wrap it in markdown, backticks, or add any extra text. There are usually 1-3 unsafe transitions in a screen.\n"
        "Response Format:\n"
        '[{“index”: <index of action>, "type": <type of unsafe transition>},'
        '...]\n\n'
        "Example output format:\n"
            "[\n"
            "  {\"index\": 12, \"type\": \"Irreversible Loss\"},\n"
            "  {\"index\": 25, \"type\": \"Unintended Modification\"},\n"
            "]"
        "Begin!!"
    )

    return sys_msg


def get_usr_prompt(screen):
    usr_msg = (
        "HTML code of the current app screen delimited by <screen> </screen>:\n"
        f"<screen>{screen}</screen>\n\n"
        "Response:\n"
    )

    return usr_msg


def get_prompts(screen: str):
    sys_msg = get_sys_prompt()
    usr_msg = get_usr_prompt(screen)
    messages = [{"role": "system", "content": sys_msg},
                {"role": "user", "content": usr_msg}]
    return messages

def get_prompts_few(screen: str):
    sys_msg = get_sys_prompt_few()
    usr_msg = get_usr_prompt(screen)
    messages = [{"role": "system", "content": sys_msg},
                {"role": "user", "content": usr_msg}]
    return messages