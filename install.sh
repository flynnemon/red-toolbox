NEWPATH="\$PATH"

echo "Gathering all script information."

for FOLDER in $(ls -d -- */)
do
	NEWPATH=$NEWPATH:$(pwd)/$(echo $FOLDER | sed 's:/*$::')
done

echo "Adding Red Toolbox scripts to your path."
echo export PATH=$NEWPATH >> ~/.zshrc
echo "Installation complete."
echo "To activate scripts run:"
echo "    source ~/.zshrc"