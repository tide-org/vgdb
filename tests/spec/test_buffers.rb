require 'spec_helper'

describe "My Vim plugin" do
  specify "some behaviour" do
    write_file('test.rb', <<-EOF)
      def foo
        bar
      end
    EOF

    vim.edit 'test.rb'
    vim.write

    IO.read('test.rb').should eq normalize_string_indent(<<-EOF)
      def foo
        bar
      end

    EOF
  end

  specify "showing vg_registers correctly" do
    write_file('test.rb', <<-EOF)
      def foo
        bar
      end
    EOF

    vim.edit 'test.rb'
    vim.write

    IO.read('test.rb').should eq normalize_string_indent(<<-EOF)
      def foo
        bar
      end

    EOF
  end
end
