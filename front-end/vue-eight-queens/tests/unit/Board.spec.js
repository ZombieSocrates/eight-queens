import { shallowMount } from '@vue/test-utils'
import Board from '@/components/Board'

describe('Board', () => {

  it('has the same number of rows as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 3
      }
    })
    console.log(`Dimension is ${testBoard.vm.dimension}`)
    const rowCount = testBoard.findAll('.row').length
    console.log(`Row count is ${rowCount}`)
    expect(rowCount).toEqual(testBoard.vm.dimension)

  })

  it('has the same number of columns as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 6
      }
    })
    console.log(`Dimension is ${testBoard.vm.dimension}`)
    const cellCount = testBoard.findAll({name: 'Cell'}).length
    const colCount = cellCount / testBoard.vm.dimension
    console.log(`Column count is ${colCount}`)
    expect(colCount).toEqual(testBoard.vm.dimension)
  })
})