import cx_Freeze

executables = [cx_Freeze.Executable("Snake.py")]

cx_Freeze.setup(name = "Snake Game", 

            options = {
                "build_exe" : {
                    "packages" : ["pygame"],
                    "include_files" : ["snakeHead.png"],
                } 
            },
            
            description = "Snake Game : Funny game",
            executables = executables

)