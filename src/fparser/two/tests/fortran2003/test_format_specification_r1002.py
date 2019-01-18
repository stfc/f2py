# Copyright (c) 2019 Science and Technology Facilities Council

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

'''Test Fortran 2003 rule R1002 : This file tests the support for a
format specification.

'''

import pytest
from fparser.two.Fortran2003 import Format_Specification, Format_Item_C1002
from fparser.two.utils import NoMatchError, InternalError


def test_single(f2003_create):
    '''Check that some basic format specifications with single format
    items are parsed correctly. Individual items are tested by the
    associated classes.

    '''
    # 1: data-edit-desc, 2: r data-edit-desc, 3: control-edit-desc, 4:
    # char-string-edit-desc, 5: format-item-list
    for my_input in ["()", "(E2.2)", "(2E2.2)", "(/)", "('hello')",
                    "(2(E2.2))"]:
        ast = Format_Specification(my_input)
        assert str(ast) == my_input


def test_multi(f2003_create):
    '''Check that a basic format specification with multiple format items
    are parsed correctly. Individual format items are tested by the
    associated classes.

    '''
    # 1: data-edit-desc, 2: r data-edit-desc, 3: control-edit-desc, 4:
    # char-string-edit-desc, 5: format-item-list
    my_input = "(E2.2, 2E2.2, /, 'hello', 2(E2.2, 'there'))"
    ast = Format_Specification(my_input)
    assert str(ast) == my_input


def test_spaces(f2003_create):
    '''Check that a basic format specification with multiple format items
    are parsed correctly with spaces. Individual format items are
    tested by the associated classes.

    '''
    # spaces before and after the brackets
    my_input = ("  (  )  ")
    ast = Format_Specification(my_input)
    # 1: data-edit-desc, 2: r data-edit-desc, 3: control-edit-desc, 4:
    # char-string-edit-desc, 5: format-item-list
    my_input = ("(  E2.2  ,  2E2.2  ,  /  ,  'hello'  ,   "
                "2(E2.2, 'there')  )")
    ast = Format_Specification(my_input)
    assert str(ast) == "(E2.2, 2E2.2, /, 'hello', 2(E2.2, 'there'))"


def test_hollerith(f2003_create):
    '''Check that a basic format specification with a hollerith string
    item is parsed correctly. Individual format items are tested by
    the associated classes.

    '''
    my_input = ("(2H,,)")
    ast = Format_Specification(my_input)
    assert str(ast) == my_input


def test_C1002(f2003_create):
    '''Check that format specifications conforming to the C1002
    constraints are parsed correctly. This test actually checks class
    Format_Item_C1002 when a comma is missing as the constraints have
    been implemented within this class in fparser.

    '''
    # Comma is optional between a P edit descriptor and an immediately
    # following F, E, EN, ES, D, or G edit descriptor, possibly
    # preceded by a repeat specifier. We only check the absence of a
    # repeat specifier for one case to cut down on the number of
    # tests.
    for specifier in ['F', 'E', 'EN', 'ES', 'D', 'G']:
        # Without repeat specifier.
        for my_input in ["(2P, {0}2.2)".format(specifier),
                         "(2P {0}2.2)".format(specifier),
                         "(2P{0}2.2)".format(specifier)]:
            ast = Format_Specification(my_input)
            assert str(ast) == "(2P, {0}2.2)".format(specifier)
        # With repeat specifier.
        for my_input in ["(2P, 2{0}2.2)".format(specifier),
                         "(2P 2{0}2.2)".format(specifier),
                         "(2P2{0}2.2)".format(specifier)]:
            ast = Format_Specification(my_input)
            assert str(ast) == "(2P, 2{0}2.2)".format(specifier)

    # Comma is optional before a slash edit descriptor when the
    # optional repeat specification is not present.
    # data-edit-desc
    for my_input in ["(2P, /)", "(2P /)", "(2P/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2P, /)"
    # control-edit-desc
    for my_input in ["(2E2.2, /)", "(2E2.2 /)", "(2E2.2/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2E2.2, /)"
    # self
    for my_input in ["(/, /)", "(/ /)", "(//)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, /)"
    # char-string-edit-desc
    for my_input in ["('hello', /)", "('hello' /)", "('hello'/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "('hello', /)"
    # format-item-list
    for my_input in ["(2(/'hello'), /)", "(2(/'hello') /)", "(2(/'hello')/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2(/, 'hello'), /)"
    # Hollerith string
    for my_input in ["(3H2.2, /)", "(3H2.2 /)", "(3H2.2/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(3H2.2, /)"
        
    # Comma is optional after a slash edit descriptor.
    # data-edit-desc
    for my_input in ["(/, 2P)", "(/ 2P)", "(/2P)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, 2P)"
    # data-edit-desc (/ with repeat specification)
    for my_input in ["(2/, 2P)", "(2/ 2P)", "(2/2P)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2/, 2P)"
    # control-edit-desc
    for my_input in ["(/, 2E2.2)", "(/ 2E2.2)", "(/2E2.2)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, 2E2.2)"
    # char-string-edit-desc
    for my_input in ["(/, 'hello')", "(/ 'hello')", "(/'hello')"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, 'hello')"
    # format-item-list
    for my_input in ["(/, 2(/'hello'))", "(/ 2(/'hello'))", "(/2(/'hello'))"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, 2(/, 'hello'))"
    # Hollerith string
    for my_input in ["(/, 3H2.2)", "(/ 3H2.2)", "(/3H2.2)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(/, 3H2.2)"

    # Comma is optional before or after a colon edit descriptor. There
    # are many combinations so just check with E : P.
    for my_input in ["(2E2.2, :, 2P)",
                     "(2E2.2 :, 2P)", "(2E2.2:, 2P)", "(2E2.2:,2P)",
                     "(2E2.2, : 2P)", "(2E2.2, :2P)", "(2E2.2,:2P)",
                     "(2E2.2 : 2P)", "(2E2.2: 2P)" ,"(2E2.2 :2P)",
                     "(2E2.2:2P)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2E2.2, :, 2P)"


def test_C1002_clash(f2003_create):
    '''The constraints rules can clash with each other. Here we test what
    happens when they do. fparser assumes that we can break the P rule,
    as does PGI. In contrast gfortran allows P / but does not allow P
    : (which seems strange).

    '''
    # P followed by : with no comma. This breaks the P rule but is
    # satisfied by the : rule.
    my_input = "(2P :)"
    ast = Format_Specification(my_input)
    assert str(ast) == "(2P, :)"
    
    # P followed by / with no comma. This breaks the P rule but is
    # satisfied by the / rule.
    my_input = "(2P /)"
    ast = Format_Specification(my_input)
    assert str(ast) == "(2P, /)"


def test_C1002_triples(f2003_create):
    '''Test that we get expected behaviour when the C1002 rule applies to
    a triplet of items.

    '''
    for my_input in ["(2P, F2.2, /)", "(2P F2.2 /)", "(2PF2.2/)"]:
        ast = Format_Specification(my_input)
        assert str(ast) == "(2P, F2.2, /)"


def test_syntaxerror(f2003_create):
    ''' Test that we get an exception for incorrect bracket syntax. '''
    for my_input in [None, "", "  ", "(", ")", "x('hello')", "('hello')x"]:
        with pytest.raises(NoMatchError):
            _ = Format_Specification(my_input)


@pytest.mark.xfail(reason="Issue #168: spaces in int-literal-constant "
                   "should not be allowed.")
def test_syntaxerror_C1002_xfail(f2003_create):
    '''This test should fail as the repeat specification for the '/' is
    present and there is no comma separating the two items. However,
    fparser treats the '3' as if it were part of the prevoious format
    specifier i.e. it outputs "(2E2.23, /)". This looks like an issue
    in utils.py/NumberBase.

    '''
    my_input = "(2E2.2 3/)"
    with pytest.raises(NoMatchError):
        _ = Format_Specification(my_input)


def test_syntaxerror_C1002(f2003_create):
    '''Test that we get an exception in situations where no comma is
    supplied and the C1002 constraints for optional commas do not
    apply.

    '''
    # Comma is mandatory before a slash edit descriptor when the
    # optional repeat specification is present
    # valid syntax
    for my_input in ["(2P, 2/)", "('hello', 2/)", "(2E2.2, 3/)"]:
        ast = Format_Specification(my_input)
    # invalid syntax
    for my_input in ["(2P 2/)", "(2P2/)", "('hello' 2/)", "('hello'2/)"]:
                    # "(2E2.2 3/)"]: to be added when previous xfail
                    # test fixed
        with pytest.raises(NoMatchError):
            _ = Format_Specification(my_input)
    # Comma is mandatory after a P descriptor if not one of ['F', 'E',
    # 'EN', 'ES', 'D', 'G'] or not a '/' or a ':'
    # Test invalid data descriptors ...
    # Valid syntax.
    for descriptor in ['I', 'B', 'O', 'Z', 'L', 'A']:
        my_input = "(2P, {0}2)".format(descriptor)
        ast = Format_Specification(my_input)
        assert str(ast) == my_input
    # Invalid syntax.
        for my_input in ["(2P {0}2)".format(descriptor),
                         "(2P{0}2)".format(descriptor)]:
            with pytest.raises(NoMatchError):
                _ = Format_Specification(my_input)
    # Check DT data descriptor
    my_input = "(2P, DT)".format(descriptor)
    ast = Format_Specification(my_input)
    assert str(ast) == my_input
    my_input = "(2P DT)".format(descriptor)
    with pytest.raises(NoMatchError):
        _ = Format_Specification(my_input)
    my_input = "(2PDT)".format(descriptor)
    with pytest.raises(NoMatchError):
        _ = Format_Specification(my_input)
    # Comma is mandatory if C1002 is not relevant
    for my_input in ["('hello' 'hello')",
                     "(2P 2P)", "(2P2P)",
                     "(F2.2 F2.2)", "(F2.2F2.2)",
                     "(T2 T2)", "(T2T2)",
                     "(('hello') ('hello'))", "(('hello')('hello'))",
                     "(2H12 3H123)", "(2H123H123)"]:
        with pytest.raises(NoMatchError):
            _ = Format_Specification(my_input)


def test_internal_errors1(f2003_create, monkeypatch):
    '''Check that an internal error is raised if the length of the Items
    list is not 2 as the str() method assumes that it is.

    '''
    line = "2P F2.2"
    ast = Format_Item_C1002(line)
    monkeypatch.setattr(ast, "items", [None, None, None])
    with pytest.raises(InternalError) as excinfo:
        str(ast)
    assert "should be of size 2 but found '3'" in str(excinfo)


def test_internal_error2(f2003_create, monkeypatch):
    '''Check that an internal error is raised if the module name (entry 0
    of items) is empty or None as the str() method assumes that it has
    content.

    '''
    line = "2P F2.2"
    ast = Format_Item_C1002(line)
    monkeypatch.setattr(ast, "items", [None, ast.items[1]])
    with pytest.raises(InternalError) as excinfo:
        str(ast)
    assert ("items entry 0 should contain a format items object but it "
            "is empty or None") in str(excinfo)


def test_internal_error3(f2003_create, monkeypatch):
    '''Check that an internal error is raised if the module name (entry 1
    of items) is empty or None as the str() method assumes that it has
    content.

    '''
    line = "2P F2.2"
    ast = Format_Item_C1002(line)
    monkeypatch.setattr(ast, "items", [ast.items[0], None])
    with pytest.raises(InternalError) as excinfo:
        str(ast)
    assert ("items entry 1 should contain a format items object but it "
            "is empty or None") in str(excinfo)
