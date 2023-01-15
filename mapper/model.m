function y = reorder(x, M, order)
    y = x;

    % Gray to binary conversion (that's right, gray to binary in modulator,
    % not vice versa!)
    if strcmp(order, 'gray')
        for i = 1:log2(M) - 1
            x = fix(x/2);
            y = bitxor(y, x);
        end
    end
end