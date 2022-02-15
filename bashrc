# put this into your ~/.bashrc script and restart the terminal

# Color Info: https://misc.flogisoft.com/bash/tip_colors_and_formatting
# prompt
FMT_BOLD="\[\e[1m\]"
FMT_DIM="\[\e[2m\]"
FMT_RESET="\[\e[0m\]"
FMT_UNBOLD="\[\e[22m\]"
FMT_UNDIM="\[\e[22m\]"
FG_BLACK="\[\e[30m\]"
FG_BLUE="\[\e[34m\]"
FG_CYAN="\[\e[36m\]"
FG_GREEN="\[\e[32m\]"
FG_GREY="\[\e[37m\]"
FG_MAGENTA="\[\e[35m\]"
FG_RED="\[\e[31m\]"
FG_WHITE="\[\e[97m\]"
BG_BLACK="\[\e[40m\]"
BG_BLUE="\[\e[44m\]"
BG_CYAN="\[\e[46m\]"
BG_GREEN="\[\e[42m\]"
BG_MAGENTA="\[\e[45m\]"

# 2nd Example 
#  PS1="\[\033[38;5;242m\]\u@\h"
#  PS1+=" \[\033[38;5;87m\]\w"
#  PS1+='\[\033[38;5;63m\]$(if git rev-parse --git-dir > /dev/null 2>&1; then echo " git("; fi)\[\033[38;5;202m\]$(git branch 2>/dev/null | grep "^*" | colrm 1 2)\[\033[38;5;63m\]$(if git rev-parse --git-dir > /dev/null 2>&1; then echo ")"; fi)'
#  PS1+="\n\[$(tput sgr0)\]└─"
#  PS1+=" \[\033[38;5;11m\]\$\[$(tput sgr0)\]"

# 3rd Example
PS1="\n ${FG_BLUE}╭─" # begin arrow to prompt
PS1+="${FG_MAGENTA}" # begin USERNAME container
PS1+="${BG_MAGENTA}${FG_CYAN}${FMT_BOLD}  " # print OS icon
PS1+="${FG_WHITE}\u" # print username
PS1+="${FMT_UNBOLD}" # end USERNAME container / begin DIRECTORY container

PS1+="\[\e[35;107m\] "
PS1+="${FG_BLACK}"
PS1+=" \d "
PS1+=" \t "
#  PS1+=" \$(find . -mindepth 1 -maxdepth 1 -type d | wc -l) " # print number of folders
#  PS1+=" \$(find . -mindepth 1 -maxdepth 1 -type f | wc -l) " # print number of files
#  PS1+=" \$(find . -mindepth 1 -maxdepth 1 -type l | wc -l) " # print number of symlinks


PS1+="${FG_WHITE}${BG_CYAN} " # end DIRECTORY container / begin FILES container
PS1+="\[\e[46m\]\[\e[30m\]\w " # print directory

PS1+="${FMT_RESET}${FG_CYAN}"
PS1+="\$(git branch 2> /dev/null | grep '^*' | colrm 1 2 | xargs -I BRANCH echo -n \"" # check if git branch exists
PS1+="${BG_GREEN} " # end FILES container / begin BRANCH container
PS1+="${FG_BLACK} BRANCH " # print current git branch
PS1+="${FMT_RESET}${FG_GREEN}\")\n " # end last container (either FILES or BRANCH)
PS1+="${FG_BLUE}╰ " # end arrow to prompt
PS1+="" # bash idk
PS1+="${FG_CYAN}\\$ " # print prompt
PS1+="${FMT_RESET}"


export PS1



