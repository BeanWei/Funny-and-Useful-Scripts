package main

import (
	"encoding/base64"
	"fmt"
	"log"
	"strings"
)

/* checkInput 检查待解析的节点链接是否符合要求 */
func checkInput(inputStr string) bool {
	if strings.HasPrefix(inputStr, "ssr://") {
		return true
	}
	return false
}

/* workUrlEncodeStr 对URL特殊字符串处理 */
func workUrlEncodeStr(urlEncodeStr string) string {
	afterWorkURL := strings.Replace(strings.Replace(urlEncodeStr, "-", "+", -1), "_", "/", -1)
	return afterWorkURL
}

/* b64Decode 将加密过的字符串进行解密 */
func b64Decode(encodeStr string) string {
	if encodeStr == "" {
		return encodeStr
	}
	/*长度不足则补等号"="*/
	paddings := len(encodeStr) % 4
	if paddings != 0 {
		paddings = 4 - paddings
	}
	for paddings > 0 {
		encodeStr += "="
		paddings--
	}
	afterWorkURL := workUrlEncodeStr(encodeStr)
	b64DecBytes, err := base64.StdEncoding.DecodeString(afterWorkURL)
	if err != nil {
		panic("Base64解码失败: " + err.Error())
	}
	b64DecStr := string(b64DecBytes)
	return b64DecStr
}

/*解析SSR链接的主函数*/
func parseSSR(encodeStr string) map[string]string {
	if checkInput(encodeStr) {
		decStr := b64Decode(encodeStr[6:])
		parts := strings.Split(decStr, ":")
		if len(parts) != 6 {
			log.Fatalln("The Input SSR Link is incomplete, can't continue parse···")
			return nil
		}

		server := parts[0]
		port := parts[1]
		protocol := parts[2]
		method := parts[3]
		obfs := parts[4]

		passwordAndParams := parts[5]
		passwordAndParamsParts := strings.Split(passwordAndParams, "/?")
		passwordEncodeStr := passwordAndParamsParts[0]
		password := b64Decode(passwordEncodeStr)

		params := passwordAndParamsParts[1]
		paramsParts := strings.Split(params, "&")
		log.Println(paramsParts)
		obfsparam := b64Decode(strings.Split(paramsParts[0], "=")[1])
		protoparam := b64Decode(strings.Split(paramsParts[1], "=")[1])
		remarks := b64Decode(strings.Split(paramsParts[2], "=")[1])
		group := b64Decode(strings.Split(paramsParts[3], "=")[1])

		SSRInfo := map[string]string{
			"server":     server,
			"port":       port,
			"protocol":   protocol,
			"method":     method,
			"password":   password,
			"obfs":       obfs,
			"obfsparam":  obfsparam,
			"protoparam": protoparam,
			"remarks":    remarks,
			"group":      group,
		}

		return SSRInfo

	}
	log.Fatalln("No support the Input SSR Link···")
	return nil

}

func main() {
	SSRLink := "ssr://MTAzLjExNC4xNjMuMzg6NTYxMzpvcmlnaW46YWVzLTI1Ni1jZmI6cGxhaW46ZDNkM0xuZDFkM2RsWWk1amIyMC8_b2Jmc3BhcmFtPSZwcm90b3BhcmFtPSZyZW1hcmtzPVFFbFNRVTVUVTFJZ0xTQXhOMEYxWnlBdElERXdNeTR4TVRRdU1UWXpMak00Jmdyb3VwPVFFbFNRVTVUVTFJ"
	SSRInfo := parseSSR(SSRLink)
	log.Println("解析成功: ")
	fmt.Printf("server: %s\n", SSRInfo["server"])
	fmt.Printf("port: %s\n", SSRInfo["port"])
	fmt.Printf("协议: %s\n", SSRInfo["protocol"])
	fmt.Printf("加密方法: %s\n", SSRInfo["method"])
	fmt.Printf("密码: %s\n", SSRInfo["password"])
	fmt.Printf("混淆: %s\n", SSRInfo["obfs"])
	fmt.Printf("混淆参数: %s\n", SSRInfo["obfsparam"])
	fmt.Printf("协议参数: %s\n", SSRInfo["protoparam"])
	fmt.Printf("备注: %s\n", SSRInfo["remarks"])
	fmt.Printf("分组: %s\n", SSRInfo["group"])
}
