# Copyright (c) 2018 Science and Technology Facilities Council

# All rights reserved.

# Modifications made as part of the fparser project are distributed
# under the following license:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Test Fortran 2008 rule R1117

    submodule-stmt is SUBMODULE ( parent-identifier ) submodule-name

'''
import pytest
from fparser.two.Fortran2003 import NoMatchError
from fparser.two.Fortran2008 import Submodule_Stmt
from fparser.two.parser import ParserFactory
# this is required to setup the fortran2008 classes
_ = ParserFactory().create(std="f2008")


def test_simple():
    ''' Test the parsing of a submodule statement'''
    result = Submodule_Stmt("submodule (id) name")
    assert str(result) == "SUBMODULE (id) name"


def test_simple_error1():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submod (id) name")
    assert "Submodule_Stmt: 'submod (id) name" in str(excinfo.value)


def test_simple_error2():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule name")
    assert "Submodule_Stmt: 'submodule name'" in str(excinfo.value)


def test_simple_error3():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule () name")
    assert "Submodule_Stmt: 'submodule () name'" in str(excinfo.value)


def test_simple_error4():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule (id)")
    assert "Submodule_Stmt: 'submodule (id)'" in str(excinfo.value)


def test_simple_error5():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule name (id)")
    assert "Submodule_Stmt: 'submodule name (id)'" in str(excinfo.value)


def test_simple_error6():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule (id) (name)")
    assert "Submodule_Stmt: 'submodule (id) (name)'" in str(excinfo.value)


def test_simple_error7():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule id) name")
    assert "Submodule_Stmt: 'submodule id) name'" in str(excinfo.value)

def test_simple_error8():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule (id name")
    assert "Submodule_Stmt: 'submodule (id name'" in str(excinfo.value)


@pytest.mark.xfail(reason="monkeypatch does not seem to work in this case")
def test_splitparen_error(monkeypatch):
    '''Test that if the first argument of the splitparen is not empty then
    an error is returned.

    '''
    def mockreturn(my_string):
        return ["XXX", "", ""]
    monkeypatch.setattr("fparser.common.splitline.splitparen", mockreturn)
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule (id) name")
    assert "Submodule_Stmt: 'submodule (id) name'" in str(excinfo.value)


@pytest.mark.xfail(reason="Does not raise an error if there is extra "
                   "content after the match")
def test_simple_error9():
    ''' Test the parsing of a submodule statement'''
    with pytest.raises(NoMatchError) as excinfo:
        _ = Submodule_Stmt("submodule (id) name :")
    assert "Submodule_Stmt: 'submodule (id) name name2'" in str(excinfo.value)
