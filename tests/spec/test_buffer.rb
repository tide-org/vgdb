require 'spec_helper'

describe "My Vim plugin" do
  specify "some behaviour" do
    write_file('test.rb', <<-EOF)
      def foo
        bar
      end
    EOF

    vim.edit 'test.rb'
    do_plugin_related_stuff_with(vim)
    vim.write

    IO.read('test.rb').should eq normalize_string_indent(<<-EOF)
      def bar
        foo
      end
    EOF
  end
end
