/system package update
check-for-updates once
:delay 1s;
:if ( [get status] = "New version is available") do={ install }