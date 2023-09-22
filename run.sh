# Get the current shell name
shell=$(ps -p $$ | tail -n 1 | awk '{print $NF}')

# Execute a command based on the shell name
if [ "$shell" = "bash" ] || [ "$shell" = "zsh" ]; then
  echo "You are using bash or zsh"
  source env/bin/activate
  python imagedownloader.py

elif [ "$shell" = "fish" ]; then
  echo "You are using fish shell"
  source env/bin/activate.fish
  python imagedownloader.py

else
  echo $" You are using some other shell.\n I don't support now.\n Just drop an issue or email me.\ I will try:)"
fi

deactivate

echo "Deactivated the env"