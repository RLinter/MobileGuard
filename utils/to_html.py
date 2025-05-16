import xml.etree.ElementTree as ET

# Global counter
counter = {"index": 0}

# Mapping XML Android classes to HTML tags
class_to_tag = {
    "android.widget.Button": "button",
    "android.widget.ImageButton": "button",
    "android.widget.TextView": "p",
    "android.widget.ScrollView": "scroll",
    "android.widget.HorizontalScrollView": "HorizontalScrollView",
    "android.widget.ImageView": "img",
    "android.widget.SeekBar": "SeekBar",
    "android.view.ViewGroup": "div",
    "android.widget.LinearLayout": "div",
    "android.widget.FrameLayout": "div",
    "android.support.v7.widget.RecyclerView": "scroll",
    "androidx.recyclerview.widget.RecyclerView": "scroll",
    "androidx.viewpager.widget.ViewPager": "scroll",
    "androidx.drawerlayout.widget.DrawerLayout": "div",
    "android.view.View": "div",
    "android.support.v7.widget.LinearLayoutCompat": "div",
    "android.view.SurfaceView": "div",
    "android.widget.RelativeLayout": "div",
    "android.widget.RadioButton": "input",
    "android.widget.GridView": "div",
    "android.widget.EditText": "input",
    "android.widget.Spinner": "select",
    "android.widget.QuickContactBadge": "img",
    "com.google.android.material.floatingactionbutton.FloatingActionButton": "button",
    "androidx.cardview.widget.CardView": "div",
    "androidx.compose.ui.platform.ComposeView": "div",
    "android.widget.AbsListView": "scroll",
    "android.widget.ViewSwitcher": "div",
    "androidx.appcompat.app.ActionBar$Tab": "div",
    "android.webkit.WebView": "iframe",
    "android.widget.CheckBox": "input",
    "android.widget.Image": "img",
    "android.widget.ListView": "scroll",
    "android.view.TextureView": "div",
    "android.widget.AutoCompleteTextView": "input",
    "androidx.appcompat.widget.LinearLayoutCompat": "div",
    # Add more mappings if needed
}

# Track missing classes
missing_classes = set()

def convert_node(node):
    global counter, missing_classes

    # Pick an HTML tag based on the Android class
    android_class = node.attrib.get('class', 'div')
    html_tag = class_to_tag.get(android_class)

    if not html_tag:
        # Warn if class is missing
        missing_classes.add(android_class)
        html_tag = "div"  # default fallback

    # Attributes for HTML
    attrs = []

    # Assign NEW global index
    attrs.append(f'index="{counter["index"]}"')
    counter["index"] += 1

    # id
    resource_id = node.attrib.get('resource-id')
    if resource_id:
        id_value = resource_id.split('/')[-1] if '/' in resource_id else resource_id
        if id_value:
            attrs.append(f'id="{id_value}"')

    # clickable
    if node.attrib.get('clickable') == 'true':
        attrs.append('clickable="true"')

    # scrollable
    if node.attrib.get('scrollable') == 'true':
        attrs.append('scrollable="true"')

    # selected
    if node.attrib.get('selected') == 'true':
        attrs.append('selected="true"')

    # content-desc
    content_desc = node.attrib.get('content-desc')
    if content_desc:
        attrs.append(f'description="{content_desc}"')

    # long-clickable
    if node.attrib.get('long-clickable') == 'true':
        attrs.append('long-clickable="true"')

    # text content
    text = node.attrib.get('text', '')

    # Build HTML open tag
    attr_string = ' '.join(attrs)
    html = f"<{html_tag} {attr_string}>"

    # Insert text if necessary
    if text.strip() and html_tag in ['p', 'button']:
        html += text.strip()

    # Process children recursively
    for child in node:
        html += convert_node(child)

    # Close tag
    html += f"</{html_tag}>"

    return html

def xml_to_html(xml_string):
    root = ET.fromstring(xml_string)
    html_output = ''
    for child in root:
        html_output += convert_node(child)
    return html_output

# Usage example
if __name__ == "__main__":
    root_path = '/Users/rui/Documents/GitHub/MobileSafety/lyft_ui_recordings'
    file_name = 'lyft_20'
    # read XML from root_path/file_name.xml
    xml_string = open(f'{root_path}/{file_name}.xml', 'r', encoding='utf-8').read()
    # xml_string = open('yourfile.xml', 'r', encoding='utf-8').read()
    html_result = xml_to_html(xml_string)

    # Save output to root_path/file_name.html
    with open(f'{root_path}/{file_name}.html', 'w', encoding='utf-8') as f:
        f.write(html_result)
    # with open('output.html', 'w', encoding='utf-8') as f:
    #     f.write(html_result)

    print("Finished generating globally indexed HTML!")

    # Warning about missing mappings
    if missing_classes:
        print("\n WARNING: Some classes had no mapping:")
        for cls in sorted(missing_classes):
            print(f"  - {cls}")
        print("\n Please update `class_to_tag` dictionary to handle these classes.")
