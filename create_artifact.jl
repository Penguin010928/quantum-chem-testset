using Tar, CodecZlib, SHA, Inflate

function create_artifact(data_dir::String, output_tar_gz::String)
    intermediate_tar = splitext(output_tar_gz)[1] * ".tar"
    Tar.create(data_dir, intermediate_tar)  # 生成未压缩的 tar
    
    open(output_tar_gz, "w") do io
        gzip_stream = GzipCompressorStream(io)
        write(gzip_stream, read(intermediate_tar))
        close(gzip_stream)
    end

    sha = open(io -> bytes2hex(sha256(io)), output_tar_gz)
    tree_hash = Tar.tree_hash(IOBuffer(inflate_gzip(output_tar_gz)))
    
    rm(intermediate_tar)
    return (sha256=sha, git_tree_sha1=tree_hash)
end

# 处理 H2
h2_hash = create_artifact("artifacts/H2_data", "artifacts/H2_data.tar.gz")
println("H2_SHA256: ", h2_hash.sha256)

# 处理 LiH
lih_hash = create_artifact("artifacts/LiH_data", "artifacts/LiH_data.tar.gz")
println("LiH_SHA256: ", lih_hash.sha256)