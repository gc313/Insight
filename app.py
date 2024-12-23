import sys
sys.path.append('./src')
import init
import layout.main as main


if __name__ == "__main__":
    init.init_database()
    #init.init_debug_data() # 初始化调试数据
    main.main_container()
    main.bottom_container()