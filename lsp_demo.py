#!/usr/bin/python3
# -------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------
import logging
import re
# import argparse
from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_TYPE_DEFINITION,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    DidSaveTextDocumentParams,
    DidCloseTextDocumentParams,
    Diagnostic,
    Range,
    Position,
    DefinitionParams,
    Location,
)

# -------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------
logging.basicConfig(filename="lsp_demo.log",
                    filemode="w",
                    format='%(asctime)-15s %(levelname)-8s%(message)s',
                    level=logging.INFO)
server = LanguageServer("lsp_demo", "v0.1")

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------

def CheckFunctionNoUser(ls, params):
    text_doc = ls.workspace.get_document(params.text_document.uri)
    logging.info(">>> Func: CheckFunctionNoUser")
    source = text_doc.source
    diagnostics = []
    # find all function name
    function = {}
    line_index = -1
    for line in source.splitlines():
        line_index += 1
        pattern = r"def\s(\w+)\("
        result = re.match(pattern, line)
        if result is not None:
            name = result.group(1)
            col_start = result.start(1)
            col_end = result.end(1)
            item = [line_index, col_start, col_end, False]
            function[name] = item

    # check function is used
    line_index = -1
    for line in source.splitlines():
        line_index += 1
        line = line.replace("(", " ")
        for word in line.split():
            if word in function:
                logging.info(">>> Item: %s, %s, %s", word, str(line_index), str(function[word][0]))
                if line_index != function[word][0]:
                    logging.info(">>> Mod: %s, change to True", word)
                    function[word][3] = True;

    # prepare response
    for key, value in function.items():
        if value[3] is False:
            logging.info(">>> Unused: ", key)
            msg = "function no used."
            d = Diagnostic(Range(Position(value[0], value[1]),
                                 Position(value[0], value[2])),
                           msg,
                           source=type(server).__name__)
            diagnostics.append(d)
    ls.publish_diagnostics(text_doc.uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """ Text document did open notification."""
    CheckFunctionNoUser(ls, params)
    logging.info(">>> Event: Text document did open")


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    CheckFunctionNoUser(ls, params)
    logging.info(">>> Event: Text document did change")


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    CheckFunctionNoUser(ls, params)
    logging.info(">>> Event: Text document did save")


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    logging.info(">>> Event: Text document did close")

@server.feature(TEXT_DOCUMENT_TYPE_DEFINITION)
def goto_definition(ls, params: DefinitionParams):
    """Jump to an object's definition."""
    logging.info(">>> Func: goto_definition")
    text_doc = ls.workspace.get_document(params.text_document.uri)
    source = text_doc.source
    # find all function name
    function = {}
    line_index = -1
    for line in source.splitlines():
        line_index += 1
        pattern = r"def\s(\w+)\("
        result = re.match(pattern, line)
        if result is not None:
            name = result.group(1)
            col_start = result.start(1)
            col_end = result.end(1)
            item = [line_index, col_start, col_end, False]
            function[name] = item
    word = text_doc.word_at_position(params.position)
    logging.info(">>> Word: ", word)

    # prepare response
    for key, value in function.items():
        if word == key:
            msg = "function no used."
            range = Range(Position(value[0], value[2] - value[1]), Position(value[0]+1, 0))
            return Location(uri=text_doc.uri, range = range)

if __name__ == "__main__":
    """
    Entry point: start the language server
    """
    logging.info("About to start lsp_demo Language Server")
    server.start_io()
    logging.info("Started lsp_demo Language Server")
