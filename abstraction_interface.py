################################################################################
#                                                                              #
# abstraction_interface                                                        #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides an interface to abstraction.                           #
#                                                                              #
# copyright (C) 2016 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

name    = "abstraction_interface"
version = "2016-06-01T1540Z"

URL     = "127.0.0.1"
socket  = "5000"

import abstraction
from flask import Flask
from flask import request
from flask import redirect

class Server(Flask):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.messages = []

server = Server(__name__)

@server.route("/")
def index():
    if server.messages:
        response = generate_response(utterance = server.messages[-1])
        server.messages.append(response)
    page = ""
    page += \
    """
    <head>
    <title>abstraction</title>
    <link
        rel="stylesheet"
        href="https://rawgit.com/wdbm/style/master/SS/darkscale.css"
        type="text/css"
    />
    <style>
    input{
        width:       740px;
        height:      90px;
    }
    textarea{
        width:       940px;
    }
    input[type=submit]{
        width:       200px;
        height:      90px;
    }
    html,
    input,
    textarea,
    pre{
        font-family: cmtex10;
        font-size:   115%;
    }
    </style>
    </head>
    <body>
    """
    page += \
    """
    <pre>ABSTRACTION INTERFACE</pre>
    <textarea
        rows="20"
        cols="80"
    >"""
    page += "&#13;&#10;".join(server.messages)
    page += \
    """</textarea>
    <form
        action="/respond"
        method="GET"><input
                         name="submit"><input
                                           type="submit" value="submit">
    </form>
    </body>
    """
    return page
 
@server.route("/respond")
def respond(): 
    # store utterance
    utterance = request.args.get("submit", "")
    server.messages.append(utterance)
    return redirect("http://" + URL + ":" + socket, code = 302)

def generate_response(
    utterance            = None,
    text_display_context = "abstraction: {text}"
    ):
        response = abstraction.generate_response(
            utterance = utterance
        )
        return text_display_context.format(text = response)

if __name__ == "__main__":
    server.run(
        host = URL,
        port = socket
    )