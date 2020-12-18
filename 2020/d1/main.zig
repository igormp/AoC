const std = @import("std");
const input = @import("input.zig").input;

pub fn main() void {
    var res: u64 = 0;
    outer: for (input) |num| {
        for (input) |num2| {
            for (input) |num3| {
                if (num + num2 + num3 == 2020) {
                    res = num * num2 * num3;
                    std.debug.print("{}\n", .{res});
                    break :outer;
                }
            }
        }
    }
}
