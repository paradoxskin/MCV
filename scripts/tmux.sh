#!/bin/bash

SESSION_NAME="main"

tmux attach-session -t $SESSION_NAME
if [ $? != 0 ]; then
  tmux new-session -s $SESSION_NAME
fi
