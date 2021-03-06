import sys

indent = " "*4

class Tag:
   def __init__(self, tag, klass=None, is_single=False, **kwargs):
      self.tag = tag
      self.children = []
      self.attributes = {}
      self.text = ""
      self.is_single = is_single

      if klass is not None:
         self.attributes["class"] = " ".join(klass)

      for attr, value in kwargs.items():
         if "_" in attr:
            attr = attr.replace("_", "-")
         self.attributes[attr] = value

   def __enter__(self):
      return self

   def __exit__(self, *args, **kwargs): pass

   def __add__(self, obj):
      self.children.append(obj)
      return self

   def __str__(self):
      clildren = ""
      attrs = []

      for attribute, value in self.attributes.items():
         attrs.append('{}="{}"'.format(attribute, value))
      attrs = " {}".format(" ".join(attrs)) if attrs else ""

      for chldrn in self.children:
         for line in str(chldrn).split("\n"):
            clildren += "{indent}{line}\n".format(line=line, indent=indent)

      if self.is_single:
         return "<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs)
      else:
         clildren = "\n{}".format(clildren) if clildren else ""
         return "<{tag}{attrs}>{text}{chld}</{tag}>".format(
                   tag=self.tag, text=self.text,
                   chld=clildren, attrs=attrs)

class HTML:
   def __init__(self, output=None):
      self.filename = output
      self.children = []

   def __enter__(self):
      return self

   def __add__(self, obj):
      self.children.append(obj)
      return self

   def __exit__(self, *argv, **kwargv):
      text = "<html>\n{chld}</html>".format( chld="".join( map(str, self.children) ) )
      if self.filename:
         print("Write to the file '{}'".format(self.filename))
         with open(self.filename, "w") as fh:
            fh.write(text)
      else:
         print(text)

class TopLevelTag:
   def __init__(self, tag):
      self.tag = tag
      self.children = []

   def __enter__(self):
      return self

   def __exit__(self, *args, **kwargs): pass

   def __add__(self, obj):
      self.children.append(obj)
      return self

   def __str__(self):
      clildren = ""
      for chldrn in self.children:
         for line in str(chldrn).split("\n"):
            clildren += "{indent}{line}\n".format(line=line, indent=indent)

      return "<{tag}>\n{chld}</{tag}>\n".format(tag=self.tag, chld=clildren)

if __name__ == "__main__":
    fileout=None
    if len(sys.argv) > 1:
       fileout = sys.argv[1]

    with HTML(output=fileout) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
