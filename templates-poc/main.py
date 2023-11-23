import cssselect2
import jinja2
import tinycss2
from lxml import etree

# Use Jinja2 to prepare template

filepath = "templates-poc/template.xml"
include_footer = True

env = jinja2.Environment()
with open(filepath) as f:
    tpl = env.from_string(f.read())
rendered = tpl.render(include_footer=include_footer)
# print(rendered)

# Use lxml to parse the xml
root: etree.Element = etree.fromstring(rendered)

# TODO: Find all <template /> elements, read and parse them and insert into the tree
# (they can include their own stylesheet refs as well)

# Find all <style /> elements and use tinycss2 to parse the styles
rules = []
for style in root.findall(".//style"):
    link = style.get("path")
    if link:
        if style.text:
            raise Exception("A <style path='...' /> element cannot contain text.")
        # TODO: link path should be relative to template path
        with open(link) as f:
            styles = f.read()
    else:
        styles = style.text

    rules.extend(tinycss2.parse_stylesheet(styles, skip_comments=True, skip_whitespace=True))


# Use cssselect2 to apply styles to each element
# NOTE: remember to also include explicit styles (eg. in a style='...'
# attribute) on each element

matcher = cssselect2.Matcher()
for rule in rules:
    selectors = cssselect2.compile_selector_list(rule.prelude)
    selector_string = tinycss2.serialize(rule.prelude)
    content_string = tinycss2.serialize(rule.content)
    payload = (selector_string, content_string)
    for selector in selectors:
        matcher.add_selector(selector, payload)

wrapper = cssselect2.ElementWrapper.from_xml_root(root.find("canvas"))
for element in wrapper.iter_subtree():
    tag = element.etree_element.tag.split("}")[-1]
    print('Found tag "{}" in XML'.format(tag))

    matches = matcher.match(element)
    if matches:
        for match in matches:
            specificity, order, pseudo, payload = match
            selector_string, content_string = payload
            print('Matching selector "{}" ({})'.format(selector_string, content_string))
    else:
        print("No rule matching this tag")
    print()

# Using an ElementFactory, transform the element tree into Element class
# instances (usually subclasses of Element), with the style applied.
# Custom elements can be registered with the ElementFactory using a
# @handle(<locator>) decorator. Tag, attributes, text (anything else?) will be
# passed into the Factory and it will return an Element (or a subclass hereof)
# instance that will be inserted into the tree.


# From this point on, the completed element tree will be passed to the Template class.
# Creating the element tree using xml/css is one option. The tree can also be
# created entirely in code.

# Compute layout using stretchable.


# Render the template.
