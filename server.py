from src.tools import mcp
 
 
def main():
    mcp.run(transport="http", host="0.0.0.0", port=8005)
 
 
if __name__ == "__main__":
    main()