# i18n Incremental File Merging

When using the angular localization it will only update the original language file, so doing incremental changes become more of a hassle. 

Using this script it will update the destination file to mirror the source file and leave all existing translations alone, all new translations will be inserted in the source language with "(NEEDS TRANSLATION)" pre-pended to it.