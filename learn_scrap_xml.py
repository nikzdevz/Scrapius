# import xml.etree.ElementTree as ET
# data = "<h2 class=\"abcde\">The Ultimate Data Science Starter Kit</h2>"
# # Load the XML file
# tree = ET.parse('data.xml')
#
# # Get the root element of the XML tree
# root = tree.getroot()


# "<?xml version="1.0" encoding="UTF-8"?>


import xml.dom.minidom
import xml.etree.ElementTree as ET

# Access and print the contents of the XML elements
# div_elements = root.getElementsByTagName('div')
# for div in div_elements:
#     div_class = div.getAttribute('class')
#     print(f"Div class: {div_class}")
#
#     h2_elements = div.getElementsByTagName('h2')
#     if h2_elements:
#         h2 = h2_elements[0]
#         h2_class = h2.getAttribute('class')
#         h2_text = h2.firstChild.nodeValue.strip()
#         print(f"H2 class: {h2_class}")
#         print(f"H2 text: {h2_text}")
#
#     p_elements = div.getElementsByTagName('p')
#     if p_elements:
#         p = p_elements[0]
#         p_class = p.getAttribute('class')
#         p_text = p.firstChild.nodeValue.strip()
#         print(f"P class: {p_class}")
#         print(f"P text: {p_text}")
#

#         ***********


myParentXml = '''
<?xml version="1.0" encoding="UTF-8"?>
<article>
  <div class="agx agy agz aha ahb l">
    <h2 class="abcde">The Ultimate Data Science Starter Kit</h2>
  </div>
  <div class="h k ud ue uf">
    <p class="efghi">Definitely master the foundational skills first before moving on to the rest. These are hand-picked courses that I feel like are most practical for you to learn the concepts.</p>
  </div>
</article>
'''
dom = ET.fromstring(myParentXml)

root = dom.getroot()
print(root)
# h2_elements = root.getElementsByTagName('h2')
# for h2 in h2_elements:
#     h2_class = h2.getAttribute('class')
#     h2_text = h2.firstChild.nodeValue.strip()
#     print(f"H2 class: {h2_class}")
#     # print(f"H2 text: {h2_text}")
#
# p_elements = root.getElementsByTagName('p')
# for p in p_elements:
#     p_class = p.getAttribute('class')
#     p_text = p.firstChild.nodeValue.strip()
#     print(f"P class: {p_class}")
