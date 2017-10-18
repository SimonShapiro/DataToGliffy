import json


class GLIFFY_SHAPES:

    RECTANGLE = {
            "uid": "com.gliffy.shape.basic.basic_v1.default.rectangle",
            "tid": "com.gliffy.stencil.rectangle.basic_v1"
        }
    COMPONENT = {
        "uid": "com.gliffy.shape.uml.uml_v2.component.component1",
        "tid": "com.gliffy.stencil.component.uml_v1"
    }
    LINE = {
        "uid": "com.gliffy.shape.uml.uml_v2.component.association",
        "tid": None
    }

class GliffyDiagram(object):
    def __init__(self):
        self.diagram = {
            "contentType": "application/gliffy+json",
            "version": "1.3",
            "stage": {
                "background": "#FFFFFF",
                "width": 306,
                "height": 308,
                "nodeIndex": 18,
                "autoFit": True,
                "exportBorder": False,
                "gridOn": True,
                "snapToGrid": False,
                "drawingGuidesOn": True,
                "pageBreaksOn": False,
                "printGridOn": False,
                "printPaper": "LETTER",
                "printShrinkToFit": False,
                "printPortrait": True,
                "maxWidth": 5000,
                "maxHeight": 5000,
                "themeData": None,
                "imageCache": None,
                "viewportType": "default",
                "fitBB": {
                    "min": {
                        "x": 10,
                        "y": 10
                    },
                    "max": {
                        "x": 306,
                        "y": 308
                    }
                },
                "printModel": {
                    "pageSize": "Letter",
                    "portrait": True,
                    "fitToOnePage": False,
                    "displayPageBreaks": False
                },
                "objects": [],
                "layers": [
                    {
                        "guid": "40FKXxnOoaFR",
                        "order": 0,
                        "name": "Layer 0",
                        "active": True,
                        "locked": False,
                        "visible": True,
                        "nodeIndex": 11
                    }
                ],
                "shapeStyles": {},
                "lineStyles": {
                    "global": {
                        "endArrow": 1
                    }
                },
                "textStyles": {}
            },
            "metadata": {
                "title": "untitled",
                "revision": 0,
                "exportBorder": False,
                "loadPosition": "default",
                "libraries": [
                    "com.gliffy.libraries.uml.uml_v2.state_machine",
                    "com.gliffy.libraries.uml.uml_v2.deployment",
                    "com.gliffy.libraries.uml.uml_v2.component",
                    "com.gliffy.libraries.uml.uml_v2.use_case",
                    "com.gliffy.libraries.mru",
                    "com.gliffy.libraries.basic.basic_v1.default",
                    "com.gliffy.libraries.flowchart.flowchart_v1.default",
                    "com.gliffy.libraries.swimlanes.swimlanes_v1.default",
                    "com.gliffy.libraries.uml.uml_v2.class",
                    "com.gliffy.libraries.uml.uml_v2.sequence",
                    "com.gliffy.libraries.uml.uml_v2.activity",
                    "com.gliffy.libraries.erd.erd_v1.default",
                    "com.gliffy.libraries.ui.ui_v3.containers_content",
                    "com.gliffy.libraries.ui.ui_v3.forms_controls",
                    "com.gliffy.libraries.images"
                ],
                "autosaveDisabled": False,
                "lastSerialized": 1507055330371,
                "analyticsProduct": "Online"
            },
            "embeddedResources": {
                "index": 0,
                "resources": []
            }
        }

class Gliff(object):
    GliffCount = 0

    def __init__(self, id: int, shape=None):
        self.gliph = {
            "x": 0,
            "y": 0,
            "rotation": 0,
            "id": id,
            "width": 100.0,
            "height": 75.0,
            "lockAspectRatio": False,
            "lockShape": False,
            "order": Gliff.GliffCount,
            "graphic": {},
            "hidden": False,
            "layer": "40FKXxnOoaFR"
        }
        Gliff.GliffCount = Gliff.GliffCount + 1
        pass

    def jsonify_gliph(self):
        return json.dumps(self.gliph)

    def set_position(self, x, y):
        self.gliph["x"] = x
        self.gliph["y"] = y
        return self

    def set_size(self, width, height):
        self.gliph["width"] = width
        self.gliph["height"] = height
        return self

    def pretty_json_string(self):
        return json.dumps(self.gliph)

    def get_size(self):
        return (self.gliph["width"], self.gliph["height"])

class Label(Gliff):  # Label on Node
    def __init__(self, id, label=None):
        Gliff.__init__(self, id)
        self.gliph["graphic"] = {
            "type": "Text",
            "Text": {
                "overflow": "none",
                "paddingTop": 8,
                "paddingRight": 8,
                "paddingBottom": 8,
                "paddingLeft": 8,
                "outerPaddingTop": 6,
                "outerPaddingRight": 6,
                "outerPaddingBottom": 2,
                "outerPaddingLeft": 6,
                "type": "fixed",
                "lineTValue": None,
                "linePerpValue": None,
                "cardinalityType": None,
                "html": "<p style=\"text-align:center;\"><span style=\"font-size:12px;font-family:Arial;text-decoration:none;\"><span style=\"text-decoration:none;\">{}</span></span></p>".format(label),
                "tid": None,
                "valign": "middle",
                "vposition": "none",
                "hposition": "none"

            }
        }
    pass


class GNode(Gliff):
    def __init__(self, id, description=None, shape=None):
        print("Initialising the gnode")
        if not description: description = id
        Gliff.__init__(self, id)
        self.gliph["uid"] = GLIFFY_SHAPES.RECTANGLE["uid"] if not shape else shape["uid"]
        self.gliph["graphic"] = {
          "type": "Shape",
          "Shape": {
            "tid": GLIFFY_SHAPES.RECTANGLE["tid"] if not shape else shape["tid"],
            "strokeWidth": 2.0,
            "strokeColor": "#333333",
            "fillColor": "#FFFFFF",
            "gradient": False,
            "dashStyle": None,
            "dropShadow": False,
            "state": 0,
            "opacity": 1.0,
            "shadowX": 0.0,
            "shadowY": 0.0
          }
        }
        self.gliph["linkMap"] = []
        label = Label(id + 1, label=description)\
            .set_size(96 , 14)\
            .set_position(2, 0)
        self.gliph["children"] = [label.gliph]  # Needs the JSON serializable data
        pass


class GLine(Gliff):
    def __init__(self, id, from_id, to_id, description=None, shape=None):
        if not description: description = id
        Gliff.__init__(self, id)
        self.gliph["uid"] = GLIFFY_SHAPES.LINE["uid"] if not shape else shape["uid"]
        self.gliph["graphic"] = {
          "type": "Line",
          "Line": {
            "strokeWidth": 1,
            "strokeColor": "#000000",
            "fillColor": "none",
            "dashStyle": None,
            "startArrow": 0,
            "endArrow": 1,
            "startArrowRotation": "auto",
            "endArrowRotation": "auto",
            "ortho": True,
            "interpolationType": "linear",
            "cornerRadius": None,
            "controlPath": [
            ],
            "lockSegments": {}
          }
        }
        self.gliph["linkMap"] = []
        label = Label(id + 1, label=description)\
            .set_size(len(str(description)) + 2, 14)\
            .set_position(2, 0)
        self.gliph["children"] = [label.gliph]  # Needs the JSON serializable data
        self.gliph["constraints"] = {
          "constraints": [],
          "startConstraint": {
            "type": "StartPositionConstraint",
            "StartPositionConstraint": {
              "nodeId": from_id,
              "px": 0.5,
              "py": 1
            }
          },
          "endConstraint": {
            "type": "EndPositionConstraint",
            "EndPositionConstraint": {
              "nodeId": to_id,
              "px": 0.5,
              "py": 0
            }
          }
        }
        pass

"""

gnode = GNode(1, description="GLIFF #10")\
    .set_position(10, 10)\
#    .set_size(110, 110)

another = GNode(2, shape=GLIFFY_SHAPES.COMPONENT)

print(json.dumps([gnode.gliph,another.gliph]))

TO DO:
1. id's to be integer
2. uid on text to be null
"""