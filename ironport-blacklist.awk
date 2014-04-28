/outbound.protection.outlook.com/ {
      icid = $10
      lastline = $0
}

($8 ~ icid && $11 ~ /BLACKLIST/ ) {

    printf "First line: %s\n",  lastline
    printf "Next line: %s\n", $0
    print ""

}
