import { shallowMount } from '@vue/test-utils'
import Board from '@/components/Board'

describe('Board', () => {

  it('has the same number of rows as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 3
      }
    })
    // const testBoard = shallowMount(Board)
    console.log(`Dimension is ${testBoard.vm.dimension}`)
    const row_count = testBoard.findAll('.row').length
    console.log(`Row count is ${row_count}`)
    expect(row_count).toEqual(testBoard.vm.dimension)

  })
})