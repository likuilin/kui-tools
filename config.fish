# ln -s (realpath config.fish) ~/.config/fish/config.fish

if status is-interactive
    # Commands to run in interactive sessions can go here

    # no truncate pwd in prompt
    set -g fish_prompt_pwd_dir_length 0

    # no truncate pwd, truncate hostname less in title
    # adapted from /usr/share/fish/functions/fish_title.fish
    function fish_title
	# emacs' "term" is basically the only term that can't handle it.
	if not set -q INSIDE_EMACS; or string match -vq '*,term:*' -- $INSIDE_EMACS
	    # If we're connected via ssh, we print the hostname.
	    set -l ssh
	    set -q SSH_TTY
	    and set ssh "["(prompt_hostname | string sub -l 20 | string collect)"]"
	    # An override for the current command is passed as the first parameter.
	    # This is used by `fg` to show the true process name, among others.
	    if set -q argv[1]
		echo -- $ssh (string sub -l 20 -- $argv[1]) (prompt_pwd)
	    else
		# Don't print "fish" because it's redundant
		set -l command (status current-command)
		if test "$command" = fish
		    set command
		end
		echo -- $ssh (string sub -l 20 -- $command) (prompt_pwd)
	    end
	end
    end

    # copy host display env, but only if we're ssh and not x forwarding
    if set -q SSH_CLIENT; and not set -q XAUTHORITY; and not set -q DISPLAY
        export (systemctl --user show-environment | grep -e ^XAUTHORITY= -e ^DISPLAY=)
    end

    # have ctrl-c on empty line not do nothing
    function custom_cancel
        set -l cmd (commandline)
        if test -n "$cmd"
            commandline -f cancel-commandline
        else
            echo -s $__fish_cancel_text
            commandline -f repaint
        end
    end
    bind \cc custom_cancel
    # run this once as $__fish_cancel_text may not exist otherwise?
    __fish_cancel_commandline

    # abbrs
    abbr -a persist-check 'sudo du -x / | grep -v ^0'
    abbr -a dc 'docker compose'
    abbr -a dclf 'docker compose logs -f'
    abbr -a dps 'docker container ls -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Size}}" | begin; sed -u 1q; sort -k2; end'

    abbr -a dnode 'docker run --rm -it node:24-alpine3.20'
    abbr -a dnodesh 'docker run --rm -it -v (pwd):/work -w /work node:24-alpine3.20 sh'
    abbr -a dpy 'docker run --rm -it python:3.13.5-alpine3.21'
    abbr -a dpysh 'docker run --rm -it -v (pwd):/work -w /work python:3.13.5-alpine3.21 sh'
end
