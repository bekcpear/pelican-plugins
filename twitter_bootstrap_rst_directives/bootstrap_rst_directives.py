#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Twitter Bootstrap RST directives Plugin For Pelican
===================================================

This plugin defines rst directives for different CSS and Javascript components from
the twitter bootstrap framework.

"""

from __future__ import unicode_literals

import sys, re

from uuid import uuid1

from html import escape
from docutils import nodes, utils
import docutils
from docutils.parsers import rst
from docutils.parsers.rst import directives, roles, Directive
from pelican import signals
from pelican.readers import RstReader, PelicanHTMLTranslator



class CleanHTMLTranslator(PelicanHTMLTranslator):

    """
        A custom HTML translator based on the Pelican HTML translator.
        Used to clean up some components html classes that could conflict
        with the bootstrap CSS classes.
        Also defines new tags that are not handleed by the current implementation of
        docutils.

        The most obvious example is the Container component
    """

    def visit_literal(self, node):
        classes = node.get('classes', node.get('class', []))
        if 'code' in classes:
            self.body.append(self.starttag(node, 'code', ''))
        elif 'file' in classes:
            self.body.append(self.starttag(node, 'code', ''))
        elif 'kbd' in classes:
            self.body.append(self.starttag(node, 'kbd', ''))
        else:
            self.body.append(self.starttag(node, 'pre'))

    def depart_literal(self, node):
        classes = node.get('classes', node.get('class', []))
        if 'code' in classes:
            self.body.append('</code>\n')
        elif 'file' in classes:
            self.body.append('</code>\n')
        elif 'kbd' in classes:
            self.body.append('</kbd>\n')
        else:
            self.body.append('</pre>\n')

    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div'))

    # def visit_raw(self, node):
    #     classes = node.get('classes', node.get('class', []))
    #     if 'ruby' in classes:
    #         self.body.append(self.starttag(node.rawtext, 'ruby'))

    # def depart_raw(self, node):
    #     classes = node.get('classes', node.get('class', []))
    #     if 'ruby' in classes:
    #         self.body.append('</ruby>\n')


class CleanRSTReader(RstReader):

    """
        A custom RST reader that behaves exactly like its parent class RstReader with
        the difference that it uses the CleanHTMLTranslator
    """

    def _get_publisher(self, source_path):
        extra_params = {'initial_header_level': '2',
                        'syntax_highlight': 'short',
                        'input_encoding': 'utf-8'}
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = docutils.core.Publisher(
            destination_class=docutils.io.StringOutput)
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = CleanHTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish()
        return pub


def keyboard_role(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    """
        This function creates an inline console input block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the kbd role

        *usage:*
            :kbd:`<your code>`

        *Example:*

            :kbd:`<section>`

        This code is not highlighted
    """
    new_element = nodes.raw(rawtext, utils.unescape("<kbd>" + text + "</kbd>", 0), format="html")
    #new_element = nodes.literal(rawtext, text, classes=['kbd'])

    return [new_element], []


def code_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :code:`<your code>`

        *Example:*

            :code:`<section>`

        This code is not highlighted
    rawtext = rawtext.replace("/", "/\u200B") # adding breakable zero width space
    text = text.replace("/", "/\u200B") # adding breakable zero width space
    """
    #new_element = nodes.literal(rawtext, text, classes=['code'])
    new_element = nodes.raw(rawtext, utils.unescape("<code>" + text + "</code>", 0), format="html")

    return [new_element], []


def file_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :file:`<file path>` <---
    rawtext = rawtext.replace("/", "/\u200B") # adding breakable zero width space
    text = text.replace("/", "/\u200B") # adding breakable zero width space
    """
    #new_element = nodes.literal(rawtext, text, classes=['file'])
    new_element = nodes.raw(rawtext, utils.unescape('<code class="file">' + text + "</code>", 0), format="html")

    return [new_element], []

# new adds
def var_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    new_element = nodes.raw(rawtext, utils.unescape('<var>' + text + '</var>', 0), format="html")
    return [new_element], []
def q_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    new_element = nodes.raw(rawtext, utils.unescape('<q>' + text + '</q>', 0), format="html")
    return [new_element], []
def samp_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    new_element = nodes.raw(rawtext, utils.unescape('<samp>' + text + '</samp>', 0), format="html")
    return [new_element], []


def ruby_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :ruby:`text|title`

    """
    rs = tuple(text.split("|"))
    if len(rs) == 2:
        content = "<ruby>%s<rp>(</rp><rt>%s</rt><rp>)</rp></ruby>" % rs
    else:
        content = "<ruby>%s<rp>(</rp><rt> Error no ruby </rt><rp>)</rp></ruby>" % text
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    new_element.source, new_element.line = inliner.reporter.get_source_and_line(lineno)
    return [new_element], []

def twi_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :twi:`userid`

    """
    new_element = nodes.reference(rawtext, "@"+text, refuri="//twitter.com/"+text)
    return [new_element], []

def pixiv_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :pixiv:`illust_id|text`

    """
    rs = tuple(text.split("|"))
    new_element = nodes.reference(rawtext, "%s (Pixiv %s)" % (rs[1], rs[0]), refuri="https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+rs[0])
    return [new_element], []


def fref_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :fref:`userid`

    """
    new_element = nodes.reference(rawtext, text, refuri="/links.html#" + (text.lower()))
    return [new_element], []


def genpkg_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :genpkg:`category/pkgname`

    """
    s = tuple(text.split("/"))
    uri = ""
    pkgname = ""
    if len(s) == 1:
        uri="https://packages.gentoo.org/packages/search?q="+s[0]
        pkgname = "<span class='name'>" + s[0] + "</span>"
    else:
        uri="https://packages.gentoo.org/packages/" + s[0] +"/" + s[1]
        pkgname = "<span class='category'>%s</span><span class='slash'>/</span><span class='name'>%s</span>" % (s[0], s[1])

    content = '<a class="reference external gentoo-package" href="%s">%s</a>' % (uri, pkgname)
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    return [new_element], []

def github_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :github:`org/reponame`

            :github:`org/reponame#issueNumber`

            :github:`org/reponame@commitHash`

            :github:`org/reponame@branch`

            :github:`org/reponame@commitHash:/path/to/file`

            :github:`org/reponame@branch:/path/to/file`

    """

    is_issue = False
    s = re.match('([\w.-]+/[\w.-]+)(#[\d]+)', text)
    if s != None:
        is_issue = True
    else:
        s = re.match('([\w.-]+/[\w.-]+)(@[\w.-]+)?(:[\S]+)?', text)

    github_reponame = s.group(1)
    github_cob = s.group(2)
    github_path = None
    if is_issue == False:
        github_path = s.group(3)

    uri = "https://github.com/" + github_reponame
    github_reponame_ele = '<span class="reponame">' + github_reponame + '</span>'

    github_cob_ele = ''
    github_path_ele = ''
    is_issue_class = ''

    if github_cob != None and is_issue == False:
        uri = uri + "/tree/" + github_cob[1:]
        github_cob_ele = '<span class="cob">'

        if re.search('^@[abcdef\d]{7,40}$', github_cob) != None:
            github_cob_ele = github_cob_ele + github_cob[1:8] + '</span>'
        else:
            github_cob_ele = github_cob_ele + github_cob[1:] + '</span>'

        if github_path != None:
            uri = uri + "/" + github_path[1:].removeprefix('/')
            github_path_ele = '<span class="path">' + github_path[1:].removeprefix('/') + '</span>'
    if is_issue:
        uri = uri + "/issues/" + github_cob[1:]
        github_cob_ele = '<span class="cob">' + github_cob[1:] + '</span>'
        is_issue_class = ' gh-issue'

    content = '<a class="reference external github%s" href="%s">%s</a>' % (is_issue_class, uri, github_reponame_ele + github_cob_ele + github_path_ele )
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    return [new_element], []

def ghpr_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :github:`org/reponame#prNumber`
    """

    s = re.match('([\w.-]+/[\w.-]+)(#[\d]+)', text)

    github_reponame = s.group(1)
    github_cob = s.group(2)

    uri = "https://github.com/" + github_reponame
    github_reponame_ele = '<span class="reponame">' + github_reponame + '</span>'

    github_cob_ele = ''

    uri = uri + "/pull/" + github_cob[1:]
    github_cob_ele = '<span class="cob">' + github_cob[1:] + '</span>'
    is_issue_class = ' gh-issue'

    content = '<a class="reference external github gh-pr" href="%s">%s</a>' % (uri, github_reponame_ele + github_cob_ele)
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    return [new_element], []



def llvmreview_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :llvmreview:`DXXXXXX`
    """

    llvmreview_id = text
    uri = "https://reviews.llvm.org/" +llvmreview_id

    content = '<a class="reference external llvmreview" href="%s">%s</a>' % (uri, text)
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    return [new_element], []

def gentoobug_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :gentoobug:`XXXXXX`
    """

    gentoobug_id = text
    uri = "https://bugs.gentoo.org/" + gentoobug_id

    content = '<a class="reference external gentoobug" href="%s">%s</a>' % (uri, 'Bug #' + gentoobug_id)
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    return [new_element], []

def pkg_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :pkg:`aur/$aurpkgname` or :pkg:`$repo/$arch/pkgname`

    """
    s = tuple(text.split("/"))
    uri = ""
    pkgname = ""
    if len(s) == 1:
        uri="https://www.archlinux.org/packages/?sort=&q="+s[0]
        pkgname = s[0]
    elif len(s) == 2:
        if s[0] == 'aur':
            uri = "https://aur.archlinux.org/packages/" + s[1] + "/"
            pkgname = s[1]
        else:
            uri="https://www.archlinux.org/packages/" + s[0] +"/x86_64/" + s[1] + "/"
            pkgname = s[1]
    else:
        uri = "https://www.archlinux.org/packages/" + s[0] +"/" + s[1] + "/" + s[2] + "/"
        pkgname = s[2]


    new_element = nodes.reference(rawtext, pkgname, refuri=uri, classes=['package'])
    return [new_element], []


def archwiki_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        *usage:*
            :archwiki:`Wiki Name` or :archwiki:`Wiki Name | Text name`

    """
    rs = tuple(text.split("|"))
    if len(rs) == 2:
        content = rs[0]
        uri = "https://wiki.archlinux.org/index.php/" + rs[0].replace(' ', '_')
    else:
        content = text
        uri = "https://wiki.archlinux.org/index.php/" + text.replace(' ', '_')

    new_element = nodes.reference(rawtext, content, refuri=uri)
    return [new_element], []



def irc_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :twi:`userid`

    """
    new_element = nodes.reference(rawtext, "#"+text, refuri="//webchat.freenode.net/?channels="+text)
    return [new_element], []


def del_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :html:`raw html`

    """
    if "|" in text:
        i = text.index("|")
        content = "<del>%s</del><ins>%s</ins>" % (text[:i], text[i + 1:])
    else:
        content = "<del>%s</del>" % text
    new_element = nodes.raw(rawtext, utils.unescape(content, 0), format="html")
    new_element.source, new_element.line = inliner.reporter.get_source_and_line(lineno)
    return [new_element], []


def html_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :html:`raw html`

    """
    new_element = nodes.raw(rawtext, utils.unescape(text, 0), format="html")
    new_element.source, new_element.line = inliner.reporter.get_source_and_line(lineno)
    return [new_element], []

def glyph_role(name, rawtext, text, lineno, inliner,
               options={}, content=[]):
    """
        This function defines a glyph inline role that show a glyph icon from the
        twitter bootstrap framework

        *Usage:*

            :glyph:`<glyph_name>`

        *Example:*

            Love this music :glyph:`music` :)

        Can be subclassed to include a target

        *Example:*

            .. role:: story_time_glyph(glyph)
                :target: http://www.youtube.com/watch?v=5g8ykQLYnX0
                :class: small text-info

            Love this music :story_time_glyph:`music` :)

    """

    target = options.get('target', None)
    glyph_name = 'glyphicon-{}'.format(text)

    if target:
        target = utils.unescape(target)
        new_element = nodes.reference(rawtext, ' ', refuri=target)
    else:
        new_element = nodes.container()
    classes = options.setdefault('class', [])
    classes += ['glyphicon', glyph_name]
    for custom_class in classes:
        new_element.set_class(custom_class)
    return [new_element], []

glyph_role.options = {
    'target': rst.directives.unchanged,
}
glyph_role.content = False

class TranslateParagraph(rst.Directive):
    has_content = True

    def create_rows(self, content):
        # return content
        result = []
        current_type = None
        current_row = []
        for i in content:
            # print(type(i), file=sys.stderr)
            if type(i) == nodes.block_quote:
                current_row.append(i.children[0])
            else:
                result.append(current_row)
                current_row = [i]
        result.append(current_row)
        return result

    def create_table_row(self, row_cells):
        row = nodes.row()
        for cell in row_cells:
            entry = nodes.entry()
            row += entry
            entry += cell
        return row

    def run(self):

        p = nodes.paragraph(text=self.content)
        self.state.nested_parse(self.content, self.content_offset, p)

        content = self.create_rows(p.children[1:])
        table = nodes.table(border=0, frame='void')

        tgroup = nodes.tgroup(cols=len(content))
        table += tgroup
        for i in range(2):
            tgroup += nodes.colspec(colwidth=1)

        # thead = nodes.thead()
        # tgroup += thead
        # thead += self.create_table_row(header)

        tbody = nodes.tbody()
        tgroup += tbody
        for data_row in content:
            tbody += self.create_table_row(data_row)

        return [table]

class TranslateLyrics(rst.Directive):
    has_content = True

    def create_rows(self, content):
        # return content
        result = []
        current_type = None
        for i in content:
            # print('---------', file=sys.stderr)
            # print('ibefore:'+ str(i), file=sys.stderr)
            if type(i) == nodes.line:
                if len(i.children) > 0:
                    i = str(i.children[0])
                else:
                    i = ""
            # print('iafter:'+ str(i), file=sys.stderr)
            # r = []
            # for x in re.split("[ 　]+", i):
            #     n = nodes.line(text=x)
            #     r.append(n)
            # if len(r)<2:
            #     r = [nodes.line(), nodes.line()]
            # print('r:'+str(r), file=sys.stderr)
            # result.append(r)
            n = nodes.line(text=i)
            # self.state.nested_parse(n, self.content_offset, n)
            result.append([n,])
        return result

    def create_table_row(self, row_cells):
        row = nodes.row()
        for cell in row_cells:
            entry = nodes.entry()
            row += entry
            entry += cell
        return row

    def run(self):

        p = nodes.line_block(text=self.content)
        self.state.nested_parse(self.content, self.content_offset, p)

        content = self.create_rows(p.children[0].children)
        table = nodes.table(border=0, frame='void')

        tgroup = nodes.tgroup(cols=len(content))
        table += tgroup
        for i in range(2):
            tgroup += nodes.colspec(colwidth=1)

        # thead = nodes.thead()
        # tgroup += thead
        # thead += self.create_table_row(header)

        tbody = nodes.tbody()
        tgroup += tbody
        for data_row in content:
            tbody += self.create_table_row(data_row)

        return [table]

class Label(rst.Directive):

    '''
        generic Label directive class definition.
        This class define a directive that shows
        bootstrap Labels around its content

        *usage:*

            .. label-<label-type>::

                <Label content>

        *example:*

            .. label-default::

                This is a default label content

    '''

    has_content = True
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        label_name = 'label-{}'.format(self.custom_class)
        # get the label content
        text = '\n'.join(self.content)
        # Create a new container element (div)
        new_element = nodes.container(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                new_element)
        # Set its custom bootstrap classes
        new_element['classes'] += ['label ', label_name]
        # Return one single element
        return [new_element]


class DefaultLabel(Label):

    custom_class = 'default'


class PrimaryLabel(Label):

    custom_class = 'primary'


class SuccessLabel(Label):

    custom_class = 'success'


class InfoLabel(Label):

    custom_class = 'info'


class WarningLabel(Label):

    custom_class = 'warning'


class DangerLabel(Label):

    custom_class = 'danger'


class Panel(rst.Directive):

    """
        generic Panel directive class definition.
        This class define a directive that shows
        bootstrap Labels around its content

        *usage:*

            .. panel-<panel-type>::
                :title: <title>

                <Panel content>

        *example:*

            .. panel-default::
                :title: panel title

                This is a default panel content

    """

    has_content = True
    option_spec = {
        'title': rst.directives.unchanged,
    }
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        panel_name = 'panel-{}'.format(self.custom_class)
        # get the label title
        title_text = self.options.get('title', self.custom_class.title())
        # get the label content
        text = '\n'.join(self.content)
        # Create the panel element
        panel_element = nodes.container()
        panel_element['classes'] += ['panel', panel_name]
        # Create the panel headings
        heading_element = nodes.container(title_text)
        title_nodes, messages = self.state.inline_text(title_text,
                                                       self.lineno)
        title = nodes.paragraph(title_text, '', *title_nodes)
        heading_element.append(title)
        heading_element['classes'] += ['panel-heading']
        # Create a new container element (div)
        body_element = nodes.container(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)
        # Set its custom bootstrap classes
        body_element['classes'] += ['panel-body']
        # add the heading and body to the panel
        panel_element.append(heading_element)
        panel_element.append(body_element)
        # Return the panel element
        return [panel_element]


class DefaultPanel(Panel):

    custom_class = 'default'


class PrimaryPanel(Panel):

    custom_class = 'primary'


class SuccessPanel(Panel):

    custom_class = 'success'


class InfoPanel(Panel):

    custom_class = 'info'


class WarningPanel(Panel):

    custom_class = 'warning'


class DangerPanel(Panel):

    custom_class = 'danger'


class Alert(rst.Directive):

    """
        generic Alert directive class definition.
        This class define a directive that shows
        bootstrap Labels around its content

        *usage:*

            .. alert-<alert-type>::

                <alert content>

        *example:*

            .. alert-warning::

                This is a warning alert content

    """
    has_content = True
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        alert_name = 'alert-{}'.format(self.custom_class)
        # get the label content
        text = '\n'.join(self.content)
        # Create a new container element (div)
        new_element = nodes.compound(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                new_element)
        # Recurse inside its children and change the hyperlinks classes
        for child in new_element.traverse(include_self=False):
            if isinstance(child, nodes.reference):
                child.set_class('alert-link')
        # Set its custom bootstrap classes
        new_element['classes'] += ['alert ', alert_name]
        # Return one single element
        return [new_element]


class SuccessAlert(Alert):

    custom_class = 'success'


class InfoAlert(Alert):

    custom_class = 'info'


class WarningAlert(Alert):

    custom_class = 'warning'


class DangerAlert(Alert):

    custom_class = 'danger'


class Friend(rst.Directive):
    has_content = True
    required_arguments = 1
    option_spec = {
        'gravatar': rst.directives.unchanged,
        'logo': rst.directives.unchanged,
        'nick': rst.directives.unchanged_required,
    }

    def run(self):
        from hashlib import md5
        # now we get the content
        text = '\n'.join(self.content)

        # get container element
        container_element = nodes.container()
        container_element['classes'] += ['media']
        container_element["ids"] += [self.arguments[0].lower()]

        # get image element
        logo_url = ''
        if 'logo' in self.options:
            logo_url = self.options['logo']
        if 'gravatar' in self.options:
            gravatar_email = self.options['gravatar'].strip().encode('utf-8')
            logo_url = 'https://www.gravatar.com/avatar/' + md5(gravatar_email).hexdigest()

        image_element = nodes.image(logo_url, alt=self.options['nick'], width="120px", **self.options)
        image_element['uri'] = logo_url
        # image_element["classes"] = ['media-object']

        image_container = nodes.container()
        image_container["classes"] += ['friend-head']
        image_container.append(image_element)

        title_text = self.options['nick']
        heading_element = nodes.container(title_text)
        title_nodes, messages = self.state.inline_text(title_text,
                                                       self.lineno)
        title = nodes.paragraph(title_text, '', *title_nodes)

        heading_element.append(title)
        heading_element['classes'] += ['media-heading', 'h5']

        # get body element
        body_container = nodes.container()
        body_element = nodes.container(text)
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)
        body_container.append(heading_element)
        body_container.append(body_element)
        body_container['classes'] += ['friend-body']

        container_element.append(image_container)
        container_element.append(body_container)
        return [container_element, ]

class Media(rst.Directive):

    '''
        generic Media directive class definition.
        This class define a directive that shows
        bootstrap media image with text according
        to the media component on bootstrap

        *usage*:
            .. media:: <image_uri>
                :position: <position>
                :alt: <alt>
                :height: <height>
                :width: <width>
                :scale: <scale>
                :target: <target>

                <text content>

        *example*:
            .. media:: http://stuffkit.com/wp-content/uploads/2012/11/Worlds-Most-Beautiful-Lady-Camilla-Belle-HD-Photos-4.jpg
                :height: 750
                :width: 1000
                :scale: 20
                :target: www.google.com
                :alt: Camilla Belle
                :position: left

                This image is not mine. Credit goes to http://stuffkit.com



    '''

    has_content = True
    required_arguments = 1

    option_spec = {
        'position': str,
        'alt': rst.directives.unchanged,
        'height': rst.directives.length_or_unitless,
        'width': rst.directives.length_or_percentage_or_unitless,
        'scale': rst.directives.percentage,
        'target': rst.directives.unchanged_required,
    }

    def get_image_element(self):
        # Get the image url
        image_url = self.arguments[0]
        image_reference = rst.directives.uri(image_url)
        self.options['uri'] = image_reference

        reference_node = None
        messages = []
        if 'target' in self.options:
            block = rst.states.escape2null(
                self.options['target']).splitlines()
            block = [line for line in block]
            target_type, data = self.state.parse_target(
                block, self.block_text, self.lineno)
            if target_type == 'refuri':
                container_node = nodes.reference(refuri=data)
            elif target_type == 'refname':
                container_node = nodes.reference(
                    refname=fully_normalize_name(data),
                    name=whitespace_normalize_name(data))
                container_node.indirect_reference_name = data
                self.state.document.note_refname(container_node)
            else:                           # malformed target
                messages.append(data)       # data is a system message
            del self.options['target']
        else:
            container_node = nodes.container()

        # get image position
        position = self.options.get('position', 'left')
        position_class = 'pull-{}'.format(position)

        container_node.set_class(position_class)

        image_node = nodes.image(self.block_text, **self.options)
        image_node['classes'] += ['media-object']

        container_node.append(image_node)
        return container_node

    def run(self):
        # now we get the content
        text = '\n'.join(self.content)

        # get image alternative text
        alternative_text = self.options.get('alternative-text', '')

        # get container element
        container_element = nodes.container()
        container_element['classes'] += ['media']

        # get image element
        image_element = self.get_image_element()

        # get body element
        body_element = nodes.container(text)
        body_element['classes'] += ['media-body']
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)

        container_element.append(image_element)
        container_element.append(body_element)
        return [container_element, ]


def register_directives():
    rst.directives.register_directive('label-default', DefaultLabel)
    rst.directives.register_directive('label-primary', PrimaryLabel)
    rst.directives.register_directive('label-success', SuccessLabel)
    rst.directives.register_directive('label-info', InfoLabel)
    rst.directives.register_directive('label-warning', WarningLabel)
    rst.directives.register_directive('label-danger', DangerLabel)

    rst.directives.register_directive('panel-default', DefaultPanel)
    rst.directives.register_directive('panel-primary', PrimaryPanel)
    rst.directives.register_directive('panel-success', SuccessPanel)
    rst.directives.register_directive('panel-info', InfoPanel)
    rst.directives.register_directive('panel-warning', WarningPanel)
    rst.directives.register_directive('panel-danger', DangerPanel)

    rst.directives.register_directive('alert-success', SuccessAlert)
    rst.directives.register_directive('alert-info', InfoAlert)
    rst.directives.register_directive('alert-warning', WarningAlert)
    rst.directives.register_directive('alert-danger', DangerAlert)

    rst.directives.register_directive('media', Media)
    rst.directives.register_directive('friend', Friend)
    rst.directives.register_directive('translate-paragraph', TranslateParagraph)
    rst.directives.register_directive('translate-lyrics', TranslateLyrics)


def register_roles():
    rst.roles.register_local_role('glyph', glyph_role)
    rst.roles.register_local_role('code', code_role)
    rst.roles.register_local_role('file', file_role)
    rst.roles.register_local_role('kbd', keyboard_role)
    rst.roles.register_local_role('var', var_role)
    rst.roles.register_local_role('q', q_role)
    rst.roles.register_local_role('samp', samp_role)
    rst.roles.register_local_role('ruby', ruby_role)
    rst.roles.register_local_role('del', del_role)
    rst.roles.register_local_role('html', html_role)
    rst.roles.register_local_role('twi', twi_role)
    rst.roles.register_local_role('pixiv', pixiv_role)
    rst.roles.register_local_role('fref', fref_role)
    rst.roles.register_local_role('irc', irc_role)
    rst.roles.register_local_role('genpkg', genpkg_role)
    rst.roles.register_local_role('github', github_role)
    rst.roles.register_local_role('ghpr', ghpr_role)
    rst.roles.register_local_role('llvmreview', llvmreview_role)
    rst.roles.register_local_role('gentoobug', gentoobug_role)
    rst.roles.register_local_role('pkg', pkg_role)
    rst.roles.register_local_role('archwiki', archwiki_role)


def add_reader(readers):
    readers.reader_classes['rst'] = CleanRSTReader


def register():
    register_directives()
    register_roles()
    #signals.readers_init.connect(add_reader) # not necessary for non-bootstrap implementation
                                              # this reader even blocks i18n
