const std = @import("std");
const Builder = std.build.Builder;

pub fn build(b: *Builder) void {
    const target = b.standardTargetOptions(.{});

    const mode = b.standardReleaseOptions();

    const run_all_step = b.step("run-all", "Run all the days");
    const total_days = 1;

    comptime var day: usize = 1;
    inline while (day <= total_days) : (day += 1) {
        const exe_name = std.fmt.allocPrint(b.allocator, "day{}", .{day}) catch unreachable;
        const run_step_name = std.fmt.allocPrint(b.allocator, "run-day{:0>2}", .{day}) catch unreachable;
        const src = std.fmt.allocPrint(b.allocator, "2020/d{}/main.zig", .{day}) catch unreachable;
        const desc = std.fmt.allocPrint(b.allocator, "Run day {:0>2}", .{day}) catch unreachable;

        const exe = b.addExecutable(exe_name, src);
        exe.setTarget(target);
        exe.setBuildMode(mode);

        const run_cmd = exe.run();
        run_cmd.step.dependOn(b.getInstallStep());

        const run_step = b.step(run_step_name, desc);
        run_step.dependOn(&run_cmd.step);
        run_all_step.dependOn(&run_cmd.step);
    }

    const exe = b.addExecutable("all", "benchmark.zig");
    exe.setTarget(target);
    exe.setBuildMode(mode);
    exe.addBuildOption(comptime_int, "days", total_days);

    const run_cmd = exe.run();
    run_cmd.step.dependOn(b.getInstallStep());

    const run_step = b.step("benchmark", "Benchmark the days");
    run_step.dependOn(&run_cmd.step);
    run_all_step.dependOn(&run_cmd.step);
}
