# Raw capture whitespace boundary

These .log files preserve exact actual process bytes. Several unittest captures
end progress lines with a space before the following diagnostic. Stripping that
space changes the independently checked native log digest. The scoped
.gitattributes marks only .log data below this evidence directory as exempt from
source-format whitespace rules; it changes no source/test or mathematical bound.
All capture bytes and their SHA256 records remain unchanged. Source formatting
checks still apply elsewhere. The initial raw-log whitespace-check failure is
retained as a preservation fact, not called a mathematical verification failure.
