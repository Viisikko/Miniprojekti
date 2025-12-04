*** Settings ***
Resource        resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${VALID_USERNAME}    outi
${VALID_PASSWORD}    12345

*** Test Cases ***
Create Reference With Valid Data and search
    Go To Add Reference Page
    Fill Reference Form
    ...    title=Clean Testing
    ...    type=book
    ...    year=2020
    ...    author=Marti A. Robot
    ...    index=MartiA.Robot2025_1
    Submit Reference Form Normally
    Wait Until Location Is    ${HOME_URL}/    5s
    Page Should Contain  Clean Testing
    Page Should Contain  book
    Page Should Contain  2020
    Page Should Contain  Marti A. Robot

    Go To Add Reference Page
    Fill Reference Form
    ...    title=Clean measing
    ...    type=book
    ...    year=2010
    ...    author=Marti A. Robot
    ...    index=MartiA.Robot2025_2
    Submit Reference Form Normally
    Wait Until Location Is    ${HOME_URL}/    5s
    Page Should Contain  Clean Testing
    Page Should Contain  book
    Page Should Contain  2010
    Page Should Contain  Marti A. Robot

    Search with name
    ...    search=measing

    Page Should not contain  2020
    Page Should contain  2010
    


*** Keywords ***
Go To Add Reference Page
    Go To    ${HOME_URL}/login
    Input Text    name:username    ${VALID_USERNAME}
    Input Text    name:password    ${VALID_PASSWORD}
    Click Button    xpath=//button[@type='submit'] | //input[@type='submit']
    Location Should Be    ${HOME_URL}/
    Go To    ${HOME_URL}/add_reference
    Location Should Be    ${HOME_URL}/add_reference

Search with name
    [Arguments]  ${search}
    Input Text  name:q  ${search}
    Click button    Search

Fill Reference Form
    [Arguments]    ${title}    ${type}    ${year}    ${author}    ${index}
    Input Text    name:title     ${title}
    Select From List By Value    name:type    ${type}
    Input Text    name:year      ${year}
    Input Text    name:author    ${author}
    Input Text    name:index     ${index}

Fill Form With Category
    [Arguments]    ${title}    ${type}    ${year}    ${author}    ${index}  ${category}
    Input Text    name:title     ${title}
    Select From List By Value    name:type    ${type}
    Input Text    name:year      ${year}
    Input Text    name:author    ${author}
    Input Text    name:index     ${index}
    Input Text    name:category     ${category}

Submit Reference Form Normally
    [Documentation]    Normal submit – HTML5 validation active.
    Click Button    Create reference
    ${loc}=    Get Location
    Log    Current URL after submit: ${loc}

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