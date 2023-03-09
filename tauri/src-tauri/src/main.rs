use std::process::Command;

 #[cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
 )]

fn main() {
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![run_anda])
   .run(tauri::generate_context!())
   .expect("error while running tauri application");
}

#[tauri::command]
fn run_anda() {
    let output = Command::new("/bin/sh")
                         .arg("-c")
                         .arg("sh /home/hallvard/fiji.sh")
                         .output()
                         .expect("failed to execute process");
    
    assert!(output.status.success());
}
