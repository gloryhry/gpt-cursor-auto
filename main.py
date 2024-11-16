from DrissionPage import ChromiumOptions, Chromium

def getTurnstileToken(tab):
    try:
        print('\n','等待验证框加载...')
        tab.wait.ele_displayed('@name=cf-turnstile-response')
        if tab.ele('@name=cf-turnstile-response'):
            print('\n',"验证框加载完成")
            challengeSolution = tab.ele("@name=cf-turnstile-response")
            challengeWrapper = challengeSolution.parent()
            challengeIframe = challengeWrapper.shadow_root.ele("tag:iframe")
            challengeIframeBody = challengeIframe.ele("tag:body")
            challengeButton = challengeIframeBody.sr("tag:input")
            challengeButton.click()
            print('\n',"验证按钮已点击，等待验证完成...")
        else:
            print('\n',"验证框未加载，跳过")      
    except Exception as e:
        print(f"处理验证失败: {str(e)}")


account = 'your_chatgpt_account'
password = 'your_chatgpt_password'

co = ChromiumOptions()

EXTENSION_PATH = ("turnstilePatch")
co.add_extension(EXTENSION_PATH) 

co.headless()
co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.92 Safari/537.36')
co.set_pref('credentials_enable_service', False)
co.set_argument('--hide-crash-restore-bubble') 
co.auto_port()

browser = Chromium(co)


"""执行登录流程"""
try:
    tab = browser.latest_tab
    tab.run_js("try { turnstile.reset() } catch(e) { }")
    print("步骤1: 开始访问网站...")

    try:
        tab.get('https://chatgpt.com')
        print('等待页面加载...')
        tab.wait.ele_displayed('t:textarea')
        if tab.ele('t:textarea'):
            print('\n','页面加载完成')
        elif tab.ele('@class=btn relative btn-blue btn-large'):
            print('\n','另一种界面加载完成')

        if tab.ele('@name=cf-turnstile-response'):
            print('\n',"准备处理验证框...")
            getTurnstileToken(tab)
            tab.wait.ele_displayed('t:textarea')
            if tab.ele('t:textarea'):
                print('\n','页面加载完成')
            elif tab.ele('@class=btn relative btn-blue btn-large'):
                print('\n','另一种界面加载完成')

    except Exception as e:
        print('\n',f"加载登录页面出错: {str(e)}")

    print('\n',"步骤2: 开始登录...")

    try:
        tab.wait(5)

        '''
        这里可以看到，先尝试直接点击登录按钮，点击按钮时会报错: 该元素没有位置及大小。
        然后尝试点击注册按钮，加载注册界面后再点击登录
        '''
        tab.wait.ele_displayed('@class=btn relative btn-primary btn-small')
        signin_btn = tab.ele('@class=btn relative btn-primary btn-small')
        if signin_btn:
            print('\n',"找到黑色登录按钮:", signin_btn.text)
        else:
            signin_btn = tab.ele('@data-testid=login-button')
            print('\n',"找到蓝色登录按钮:", signin_btn.text)
        try:    
            signin_btn.click()
        except Exception as e:
            print(f"处理登录按钮时出错: {str(e)}")

        tab.wait.ele_displayed('@class=btn relative btn-secondary btn-small')
        signup_btn = tab.ele('@class=btn relative btn-secondary btn-small')
        if signup_btn:
            print('\n',"找到注册按钮:", signup_btn.text)
            signup_btn.click()
        print('\n',"点击注册按钮")

        tab.wait.ele_displayed('@class=other-page-link')
        signin_btn = tab.ele('@class=other-page-link')
        if signin_btn:
            print('\n',"找到跳转登录链接:", signin_btn.text)
            signin_btn.click()
            print('\n',"点击跳转登录链接")
        else:
            print('\n',"准备处理验证框...")
            getTurnstileToken(tab)
            tab.wait.ele_displayed('@class=other-page-link')
            signin_btn = tab.ele('@class=other-page-link')
            if signin_btn:
                print('\n',"找到跳转登录链接:", signin_btn.text)
                signin_btn.click()
                print('\n',"点击跳转登录链接")
                
    except Exception as e:
        print(f"处理注册按钮时出错: {str(e)}")
    
    tab.wait(2)
    print('\n',"步骤3: 输入邮箱...")
    try:
        tab.wait.ele_displayed('@id=email-input')
        if tab.ele('@id=email-input'):
            print('\n',"邮箱输入框加载完成")
        tab.actions.click('@id=email-input').type(account)
        tab.wait(0.5)
        tab.ele('@class=continue-btn').click()
        print('\n',"输入邮箱并点击继续")
    except Exception as e:
        print(f"加载邮箱输入框时出错: {str(e)}")

    tab.wait(5)
    print('\n',"步骤4: 输入密码...")
    try:
        # tab.wait.ele_displayed('获取您的 SSO 信息时出错')
        # if tab.ele('获取您的 SSO 信息时出错'):
        tab.wait.ele_displayed('@class=title-wrapper')
        title_element = tab.ele('@class=title-wrapper')
        if title_element and "获取您的 SSO 信息时出错" in title_element.text:
            print('\n','检测到 SSO 错误，脚本终止，请手动登录')
            exit()

        tab.wait.ele_displayed('@id=password')
        if tab.ele('@id=password'):
            print('\n',"密码输入框加载完成")
        else:
            print('\n',"准备处理验证框...")
            getTurnstileToken(tab)
            tab.wait.ele_displayed('@id=password')
            if tab.ele('@id=password'):
                print('\n',"密码输入框加载完成")
            
        tab.actions.click('@id=password').input(password)
        tab.wait(2)    
        tab.actions.click('@type=submit')
        print('\n',"输入密码并点击登录")
    except Exception as e:
        print(f"再次输入邮箱时出错: {str(e)}")

    tab.wait(5)
    print('\n',"步骤5: 获取access_token...")

    tab.wait.ele_displayed('有什么可以帮忙的？')
    help = tab.ele('有什么可以帮忙的？')
    if help:
        print('\n','登录成功！')
    else:
        print('\n','登录可能遇到问题')

    tab.wait.ele_displayed('重新发送电子邮件')
    verify_code = tab.ele('重新发送电子邮件')
    if verify_code:
        print('\n','提示需要邮箱验证码，脚本终止，请手动获取')
        exit()

    browser.new_tab('https://chatgpt.com/api/auth/session')
    tab = browser.latest_tab
    tab.wait(1)
    response_json = tab.json
    if response_json and 'accessToken' in response_json:
        access_token = response_json['accessToken']
        print('\n',"请复制保存你的access_token:",'\n')
        print(access_token)
    else:
        print("错误:未找到access token")

except Exception as e:
    print(f"发生错误的完整信息: {str(e)}")
    import traceback
    print(f"错误堆栈: {traceback.format_exc()}")
finally:
    input("\n按Enter键关闭浏览器...")
    browser.quit()
  
