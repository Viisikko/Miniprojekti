*** Settings ***
Resource        resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${VALID_USERNAME}    outi
${VALID_PASSWORD}    12345

*** Test Cases ***
Create Reference With Valid Data
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Clean Code
    ...    type=book
    ...    year=2008
    ...    author=Robert C. Martin
    Submit Reference Form Normally
    Location Should Be    ${HOME_URL}/
    Page Should Not Contain    Error:

Create Reference Fails With Empty Title
    [Documentation]    Backend should reject empty title (after strip()).
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Some Title
    ...    type=book
    ...    year=2000
    ...    author=Some Author
    Set Title Value Via Javascript    ${EMPTY}
    Submit Form Bypassing Html5 Validation
    Page Should Contain    Error: Title must be between 1 and 64 characters.

Create Reference Fails With OutOfRange Year
    [Documentation]    Backend should reject year < 868.
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Ancient Book
    ...    type=book
    ...    year=2000
    ...    author=Old Author
    Set Year Value Via Javascript    500
    Submit Form Bypassing Html5 Validation
    Page Should Contain    Error: Year cannot be under 868 or too much in the future.

Create Reference Fails With Invalid Type
    [Documentation]    Backend should reject type != 'book'.
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Some Title
    ...    type=book
    ...    year=2020
    ...    author=Some Author
    Set Type Value Via Javascript    article
    Submit Form Bypassing Html5 Validation
    Page Should Contain    Error: Invalid type.

Create Reference Fails With TooShortAuthor
    [Documentation]    Backend should reject author shorter than 3 chars.
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Short Author Test
    ...    type=book
    ...    year=2020
    ...    author=Some Author
    Set Author Value Via Javascript    Al
    Submit Form Bypassing Html5 Validation
    Page Should Contain    Error: Author must be at least 3 characters long.


*** Keywords ***
Go To Add Reference Page
    Go To    ${HOME_URL}/login
    Input Text    name:username    ${VALID_USERNAME}
    Input Text    name:password    ${VALID_PASSWORD}
    Click Button    xpath=//button[@type='submit'] | //input[@type='submit']
    Location Should Be    ${HOME_URL}/
    Go To    ${HOME_URL}/add_reference
    Location Should Be    ${HOME_URL}/add_reference

Fill Reference Form
    [Arguments]    ${title}    ${type}    ${year}    ${author}
    Input Text    name:title     ${title}
    Select From List By Value    name:type    ${type}
    Input Text    name:year      ${year}
    Input Text    name:author    ${author}

Submit Reference Form Normally
    [Documentation]    Normal submit – HTML5 validation active.
    Click Button    Create reference

Set Title Value Via Javascript
    [Arguments]    ${value}
    ${script}=    Set Variable    document.querySelector('input[name="title"]').value = "${value}";
    Execute Javascript    ${script}

Set Year Value Via Javascript
    [Arguments]    ${value}
    ${script}=    Set Variable    document.querySelector('input[name="year"]').value = "${value}";
    Execute Javascript    ${script}

Set Type Value Via Javascript
    [Arguments]    ${value}
    ${script}=    Set Variable    document.querySelector('select[name="type"]').value = "${value}";
    Execute Javascript    ${script}

Set Author Value Via Javascript
    [Arguments]    ${value}
    ${script}=    Set Variable    document.querySelector('input[name="author"]').value = "${value}";
    Execute Javascript    ${script}

Submit Form Bypassing Html5 Validation
    [Documentation]    Use native form.submit() to skip browser constraint validation entirely.
    ${script}=    Set Variable    document.querySelector('form[action="/create_reference"]').submit();
    Execute Javascript    ${script}
