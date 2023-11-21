from abc import ABC, abstractmethod

from stretchable import Node

"""

There should be a central RenderManager, which provides figure, axes, etc.
Convenience methods on elements request axes etc. from the render manager.

Should model be passed into *render methods, what about other parameters?
Or should model/parameters be provided by RenderManager? Or ModelProvider?

So the pipeline would be:

1) Register/select model data/args with ModelProvider
2) RenderManager.render(canvas)
    - Invoke pre-render to prepare for measuring
    - Compute layout and position all elements
    - Invoke render
    - Invoke post-render

TODO:
 - List requirements
 - List of report/plot types that must be supported/facilitated (single/multi
   page for single or multiple models/entities, etc.)
 - Make a simple prototype/example of how the above would look. Considering various types of canvas/templates.



"""


class Element(ABC, Node):
    ...

    def pre_render(self, **args) -> None:
        """This method is called prior to positioning of elements. Any
        preprocessing of model data necessary for measuring the element should
        be done here, so measuring can be as fast as possible. Pre-rendering is
        optional."""

    def measure(self):
        """This should be optional, but only if the size of the element is
        specified statically using style."""

    @abstractmethod
    def render(self, **args) -> None:
        """This method should perform the actual rendering."""

    def post_render(self, **args) -> None:
        """This method is called after rendering the model data, eg. can be used
        for cleanup/teardown. Post-rendering is optional."""
