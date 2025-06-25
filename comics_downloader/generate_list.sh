category="$1"
curl -s https://readallcomics.com/category/${category}/ | grep -Eo 'href="https://readallcomics\.com/'"${category}"'[^"]+'  | sed 's/href="https:\/\/readallcomics.com\///' | sed 's/\/$//'
