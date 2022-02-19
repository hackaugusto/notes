use std::fs::File;
use std::io::prelude::*;

static MAGIC: &[u8; 4] = b"\x7fELF";
static FORMAT64: &[u8; 1] = b"\x02";
static LITTLE_ENDIAN: &[u8; 1] = b"\x01";
static EI_VERSION1: &[u8; 1] = b"\x01";
static ABI_LINUX: &[u8; 1] = b"\x03";
static EIPAD: &[u8; 8] = b"\x00\x00\x00\x00\x00\x00\x00\x00";
static EXECUTABLE: &[u8; 2] = b"\x02\x00";
static AMD64: &[u8; 2] = b"\x3E\x00";
static E_VERSION1: &[u8; 4] = b"\x01\x00\x00\x00";
static E_FLAGS: &[u8; 4] = b"\x00\x00\x00\x00";
static HEADER_SIZE: &[u8; 2] = b"\x40\x00";

static LOAD: &[u8; 4] = b"\x01\x00\x00\x00";
static RX: &[u8; 4] = b"\x05\x00\x00\x00";
static PHYSICAL_ADDRESS: &[u8; 8] = b"\x00\x00\x00\x00\x00\x00\x00\x00";

fn main() -> std::io::Result<()> {
    let mut file = File::create("a.out")?;
    let program: &[u8] = b"\x66\xbf\x2a\x00\x31\xc0\xb0\x3c\x0f\x05";
    let entry_offset: &[u8; 8] = b"\x78\x80\x04\x08\x00\x00\x00\x00";
    // offset right after ELF header
    let program_header_offset: &[u8; 8] = b"\x40\x00\x00\x00\x00\x00\x00\x00";
    let section_header_offset: &[u8; 8] = b"\x00\x00\x00\x00\x00\x00\x00\x00";

    // (4 + 4) + (8 + 8 + 8) + (8 + 8 + 8)
    let program_header_entry_size: &[u8; 2] = b"\x38\x00";
    let program_header_num_entries: &[u8; 2] = b"\x01\x00";

    let section_header_entry_size: &[u8; 2] = b"\x00\x00";
    let section_header_num_entries: &[u8; 2] = b"\x00\x00";
    let section_names: &[u8; 2] = b"\x00\x00";

    file.write_all(MAGIC)?;
    file.write_all(FORMAT64)?;
    file.write_all(LITTLE_ENDIAN)?;
    file.write_all(EI_VERSION1)?;
    file.write_all(ABI_LINUX)?;
    file.write_all(EIPAD)?;
    file.write_all(EXECUTABLE)?;
    file.write_all(AMD64)?;
    file.write_all(E_VERSION1)?;
    file.write_all(entry_offset)?;
    file.write_all(program_header_offset)?;
    file.write_all(section_header_offset)?;
    file.write_all(E_FLAGS)?;
    file.write_all(HEADER_SIZE)?;
    file.write_all(program_header_entry_size)?;
    file.write_all(program_header_num_entries)?;
    file.write_all(section_header_entry_size)?;
    file.write_all(section_header_num_entries)?;
    file.write_all(section_names)?;

    let program_offset: &[u8; 8] = b"\x00\x00\x00\x00\x00\x00\x00\x00";
    let virtual_address: &[u8; 8] = b"\x00\x80\x04\x08\x00\x00\x00\x00";
    let file_size_bytes = program.len().to_ne_bytes();
    let file_size = &file_size_bytes;
    let mem_size = &file_size_bytes;
    let align = b"\x00\x00\x00\x00\x00\x00\x00\x00";
    file.write_all(LOAD)?;
    file.write_all(RX)?;
    file.write_all(program_offset)?;
    file.write_all(virtual_address)?;
    file.write_all(PHYSICAL_ADDRESS)?;
    file.write_all(file_size)?;
    file.write_all(mem_size)?;
    file.write_all(align)?;

    file.write_all(program)?;

    Ok(())
}
