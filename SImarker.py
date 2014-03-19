import xml.dom.minidom

def generate_dataset():
    doc = xml.dom.minidom.parse("output.xml")
    preps = doc.getElementsByTagName("PREPOSITION")
    multiwords = 0
    uniwords = 0
    redundancies = 0
    for prep in preps:
        classnode = doc.createElement("CLASS")
        tag = "NSI"
        prep_index=prep.getAttribute("id")
        preptext = prep.getElementsByTagName("PREP")[0].childNodes[0].data
        sis = prep.parentNode.parentNode.getElementsByTagName("SPATIAL_INDICATOR")
        sentence = prep.parentNode.parentNode.getElementsByTagName("CONTENT")[0].childNodes[0].data
        index="garbage"
        for si in sis:
            sitext = si.childNodes[0].data.split() # split to delete spureous white spaces
            temp_index=si.childNodes[0].getAttribute("id")
            index=temp_index[2:]
            if len(sitext) > 1: multiwords +=1
            else: uniwords +=1

            sitext = " ".join(sitext)
            if index == prep_index:
                tag = "SI"
        textnode = doc.createTextNode(tag)
        classnode.appendChild(textnode)
        prep.appendChild(classnode)

    f = open('SItrain.xml', 'w')
    doc.writexml(f)
    f.close()
if __name__ == "__main__":
    generate_dataset()
